import pygame
import circleshape
from constants import LINE_WIDTH, ASTEROID_MIN_RADIUS
from logger import log_event
import random


class Asteroid(circleshape.CircleShape):

    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, surface):
        return pygame.draw.circle(surface, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            log_event("asteroid_split")
            new_angle = random.uniform(20.0, 50.0)
            first_dir = self.velocity.rotate(new_angle)
            second_dir = self.velocity.rotate(-new_angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            small_asteroid_one = Asteroid(*self.position, new_radius)
            small_asteroid_two = Asteroid(*self.position, new_radius)
            small_asteroid_one.velocity = first_dir * 1.2
            small_asteroid_two.velocity = second_dir * 1.2
