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

IDEAL_WIDTH = 700
IDEAL_HEIGHT = 900

TILE_WIDTH = 0

HORIZ_TILES = 10
VERT_TILES = 10

PALETTE = [(1, 1, 1), (10, 255, 78)]

ARRAY = [[0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0],
         [0, 1, 0, 1, 0, 1, 0, 1, 0, 1], [1, 0, 1, 0, 1, 0, 1, 0, 1, 0], [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
         [1, 0, 1, 0, 1, 0, 1, 0, 1, 0]]
fg = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

CURRENT_COLOR = 0

NEED_UPDATE = True

BUFFER = 1


def tile_to_point(tile):
    global TILE_WIDTH, BUFFER
    return (tile[0] + BUFFER) * TILE_WIDTH, (tile[1] + BUFFER) * TILE_WIDTH


def point_to_tile(point):
    global TILE_WIDTH, BUFFER
    return math.floor((point[0] / TILE_WIDTH) - BUFFER), math.floor((point[1] / TILE_WIDTH) - BUFFER)


def get_pixels():
    global ARRAY, TILE_WIDTH
    pixels = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA).convert()
    pixels.set_colorkey(CLR)
    for x in range(0, len(ARRAY)):
        for y in range(0, len(ARRAY[x])):
            pygame.draw.rect(pixels, PALETTE[ARRAY[x][y]],
                             pygame.Rect(tile_to_point((x, y)), (TILE_WIDTH, TILE_WIDTH)))
    return pixels


def ints_from_byte_file(filename):
    file = open(filename, "rb")
    ints = file.read()
    file.close()
    return ints


def ints_to_byte_file(filename, ints):
    file = open(filename, "wb")
    file.write(bytes(ints))
    file.close()


class Lines:
    def __init__(self):
        self.start_points = [(175, 0), (325, 0), (475, 0), (625, 0)]
        self.end_points = [(175, SCREEN_HEIGHT), (325, SCREEN_HEIGHT), (475, SCREEN_HEIGHT), (625, SCREEN_HEIGHT)]

    def draw(self, surf):
        if self.num_of_lines > 0:
            for i in range(0, self.num_of_lines):
                pygame.draw.line(surf, WHITE, self.start_points[i], self.end_points[i])


def main():
    global PALETTE, CURRENT_COLOR, ARRAY, NEED_UPDATE, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, IDEAL_WIDTH, IDEAL_HEIGHT

    TILE_WIDTH = int(min(IDEAL_WIDTH / (HORIZ_TILES + 2 * BUFFER), IDEAL_HEIGHT / (VERT_TILES + 2 * BUFFER)))
    if TILE_WIDTH % 2 == 1:
        TILE_WIDTH -= 1
    SCREEN_WIDTH = TILE_WIDTH * (HORIZ_TILES + 2 * BUFFER)
    SCREEN_HEIGHT = TILE_WIDTH * (VERT_TILES + 2 * BUFFER)
    print(TILE_WIDTH)
    print(tile_to_point((0, 0)))
    print(point_to_tile((0, 0)))
    pygame.init()

    screen = pygame.display.set_mode([SCREEN_WIDTH, SCREEN_HEIGHT])

    pixels = get_pixels()

    pygame.display.set_caption("Sprite Maker")

    working = True

    holding = False

    background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
    background.fill(BLACK)

    clock = pygame.time.Clock()

    while working:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                working = False

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_p:
                    user_in = input("[Palette] Import or export?")
                    if user_in.lower().startswith("i"):
                        user_in = input("[Import Palette] What is the filename?")
                        ints = ints_from_byte_file(user_in)
                        PALETTE = []
                        for i in range(1, ints[0]+1):
                            PALETTE.append((ints[3*(i-1) + 1], ints[3*(i-1) + 2], ints[3*(i-1) + 3]))
                        print("[Import Palette] Done!")
                        NEED_UPDATE = True
                    else:
                        user_in = input("[Export Palette] What is the desired filename?")
                        ints = [] # TODO: Could be implemented better
                        for color in PALETTE:
                            ints.append(color[0])
                            ints.append(color[1])
                            ints.append(color[2])
                        ints_to_byte_file(user_in, ints)
                        print("[Export Palette] Done!")
                        NEED_UPDATE = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # add ability to change selected color
                holding = True

            if event.type == pygame.MOUSEBUTTONUP:
                # add ability to change selected color
                holding = False

        if holding:
            tile = point_to_tile(pygame.mouse.get_pos())
            print(tile)
            if 0 <= tile[0] < HORIZ_TILES and 0 <= tile[1] < VERT_TILES and not ARRAY[tile[0]][
                                                                                    tile[1]] == CURRENT_COLOR:
                ARRAY[tile[0]][tile[1]] = CURRENT_COLOR
                NEED_UPDATE = True
        screen.blit(background, (0, 0))

        if NEED_UPDATE:
            pixels = get_pixels()
            NEED_UPDATE = False

        screen.blit(pixels, (0, 0))
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
