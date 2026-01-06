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
        self.invulnerability = False
        self.speed = PLAYER_SPEED

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]

    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt


    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.cooldown -= dt
        if keys[pygame.K_a]:
            self.rotate(-dt)
        elif keys[pygame.K_d]:
            self.rotate(dt)
        elif keys[pygame.K_w]:
            self.move(dt)
            self.speed += ACCELERATION_SPEED
        elif keys[pygame.K_s]:
            self.speed -= ACCELERATION_SPEED
        elif keys[pygame.K_SPACE]:
            self.shoot()
        else:
            self = PLAYER_SPEED

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * self.speed * dt
        self.position += rotated_with_speed_vector


    def shoot(self):
        if self.cooldown <= 0:
            self.cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS
            shot = Shot(*self.position, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.score += 1


