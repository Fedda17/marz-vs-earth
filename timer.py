import pygame
from constants import TIMED_MISSION

class Timer(pygame.font.Font):

    def __init__(style, size):
        super().__init__(style, size)
        self.start = TIMED_MISSION
        