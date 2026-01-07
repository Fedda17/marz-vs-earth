import pygame
import circleshape
from shot import Shot
from constants import *

class Player(circleshape.CircleShape):
    
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.cooldown = 0
        self.score = 0
        self.health = MAX_HEALTH
        self.game_over = False
        self.invulnerability = 0.0

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, keys, dt):
        if keys[pygame.K_a]:
            self.rotation += PLAYER_TURN_SPEED * dt
        elif keys[pygame.K_d]:
            self.rotation += PLAYER_TURN_SPEED * -dt


    def take_damage(self, other):
        if self.invulnerability <= 0:
            self.invulnerability = PLAYER_INVULNERABILITY
            self.health -= 1.2 * other.radius
        if self.health <= 0:
            self.game_over = True



    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt
        self.invulnerability -= dt
        self.movement(keys, dt)
        self.rotate(keys, dt)
        self.shoot(keys)

            
    def movement(self, keys, dt):
        if keys[pygame.K_w]:
            unit_vector = pygame.Vector2(0, 1)
            rotated_vector = unit_vector.rotate(self.rotation)
            rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
            self.position += rotated_with_speed_vector + self.velocity


    def shoot(self, keys):
        if keys[pygame.K_SPACE]:
            if self.cooldown <= 0:
                self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
                shot = Shot(*self.position, SHOT_RADIUS)
                shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED


