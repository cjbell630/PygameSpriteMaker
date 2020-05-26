import pygame
import math
import numpy
import random

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (100, 100, 255)
GOLD = (255, 215, 0)
PURPLE = (175, 135, 255)
CLR = (1, 1, 1)

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 850

HORIZ_PIXELS = 10

VERT_PIXELS = 10



def get_background():
    background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
    background.fill(BLACK)
    x = 100
    for c in [BLUE, PURPLE, BLUE, PURPLE]:
        pygame.draw.rect(background, c, (x, 0, 150, SCREEN_HEIGHT))
        pygame.draw.rect(background, (c[0] - 50, c[1] - 50, c[2] - 50), (x, 0, 150, 130))
        pygame.draw.rect(background, (c[0] - 50, c[1] - 50, c[2] - 50), (x, SCREEN_HEIGHT - 130, 150, 130))
        x += 150
    return background


class Lines:
    def __init__(self):
        self.start_points = [(175, 0), (325, 0), (475, 0), (625, 0)]
        self.end_points = [(175, SCREEN_HEIGHT), (325, SCREEN_HEIGHT), (475, SCREEN_HEIGHT), (625, SCREEN_HEIGHT)]
        self.num_of_lines = 4
        self.temp_start = (-1, -1)
        self.temp_end = (-1, -1)

    def clear(self):
        self.start_points = [(175, 0), (325, 0), (475, 0), (625, 0)]
        self.end_points = [(175, SCREEN_HEIGHT), (325, SCREEN_HEIGHT), (475, SCREEN_HEIGHT), (625, SCREEN_HEIGHT)]
        self.num_of_lines = 4

    def draw(self, screen):
        if self.num_of_lines > 0:
            for i in range(0, self.num_of_lines):
                pygame.draw.line(screen, WHITE, self.start_points[i], self.end_points[i])
        if self.temp_start[0] != -1:
            pygame.draw.line(screen, WHITE, self.temp_start, self.temp_end)
            self.temp_start = (-1, -1)


def main():
    global points

    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    pygame.display.set_caption("Mario's Slides")

    working = True

    background = get_background()

    clock = pygame.time.Clock()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False

            if event.type == pygame.MOUSEBUTTONDOWN:


        screen.blit(background, (0, 0))

        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
