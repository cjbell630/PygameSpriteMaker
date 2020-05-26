import pygame
import math
import os
import sys
import psutil
import logging

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

BG_COLOR = 0
BG_COLORS = [BLACK, GREEN, GOLD, RED, BLUE, PURPLE]

GRID = True

FILENAME = None

PALETTE = [(1, 1, 1), (10, 255, 78), (10, 10, 78)]

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


# https://stackoverflow.com/a/33334183/12861567
def restart_program():
    """Restarts the current program, with file objects and descriptors
       cleanup
    """

    try:
        p = psutil.Process(os.getpid())
        for handler in p.open_files() + p.connections():
            os.close(handler.fd)
    except Exception as e:
        logging.error(e)

    python = sys.executable
    os.execl(python, python, *sys.argv)


def tile_to_point(tile):
    global TILE_WIDTH, BUFFER
    return (tile[0] + BUFFER) * TILE_WIDTH, (tile[1] + BUFFER) * TILE_WIDTH


# https://www.geeksforgeeks.org/python-ways-to-concatenate-two-lists/
def combine_arrays(a1, a2):
    return [y for x in [a1, a2] for y in x]


def point_to_tile(point):
    global TILE_WIDTH, BUFFER
    return math.floor((point[0] / TILE_WIDTH) - BUFFER), math.floor((point[1] / TILE_WIDTH) - BUFFER)


def get_pixels():
    global ARRAY, TILE_WIDTH, PALETTE
    pixels = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA).convert()
    pixels.fill(CLR)
    pixels.set_colorkey(CLR)
    for x in range(0, len(ARRAY)):
        for y in range(0, len(ARRAY[x])):
            pygame.draw.rect(pixels, PALETTE[ARRAY[x][y]],
                             pygame.Rect(tile_to_point((x, y)), (TILE_WIDTH, TILE_WIDTH)))
    return pixels


def get_palette_display(selected):
    palette_display = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA).convert()
    palette_display.fill(CLR)
    palette_display.set_colorkey(CLR)
    for i in range(0, len(PALETTE)):
        if (i == selected):
            pygame.draw.rect(palette_display, GREEN,
                             pygame.Rect((TILE_WIDTH * (i + 0.385), TILE_WIDTH * 0.385),
                                         (TILE_WIDTH * 0.75, TILE_WIDTH / 4)))
        if PALETTE[i][0] == 1 and PALETTE[i][1] == 1 and PALETTE[i][2] == 1:
            pygame.draw.rect(palette_display, WHITE,
                             pygame.Rect((TILE_WIDTH * (i + 0.5), TILE_WIDTH / 4), (TILE_WIDTH / 2, TILE_WIDTH / 2)))
            palette_display.blit(
                pygame.font.Font('freesansbold.ttf', 10).render("CLR", True, BLACK), (TILE_WIDTH / 2, TILE_WIDTH / 4))
        else:
            pygame.draw.rect(palette_display, PALETTE[i],
                             pygame.Rect((TILE_WIDTH * (i + 0.5), TILE_WIDTH / 4), (TILE_WIDTH / 2, TILE_WIDTH / 2)))

    return palette_display


def get_grid():
    grid = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT], pygame.SRCALPHA).convert()
    grid.fill(CLR)
    grid.set_colorkey(CLR)
    for x in range(0, HORIZ_TILES + 1):
        pygame.draw.line(grid, WHITE, tile_to_point((x, 0)), tile_to_point((x, VERT_TILES)))
    for y in range(0, VERT_TILES + 1):
        pygame.draw.line(grid, WHITE, tile_to_point((0, y)), tile_to_point((HORIZ_TILES, y)))
    return grid


def get_background():
    background = pygame.Surface([SCREEN_WIDTH, SCREEN_HEIGHT])
    background.fill(BG_COLORS[BG_COLOR])
    return background


def ints_from_byte_file(filename):
    file = open("files/" + filename, "rb")
    ints = []
    for b in file.read():
        ints.append(int(b))
    file.close()
    return ints


def ints_to_byte_file(filename, ints):
    file = open("files/" + filename, "wb")
    file.write(bytes(ints))
    file.close()


def palette_to_int_array():
    ints = []  # TODO: Could be implemented better
    for color in PALETTE:
        ints.append(color[0])
        ints.append(color[1])
        ints.append(color[2])
    return ints


def sprite_to_int_array():
    global PALETTE, ARRAY, HORIZ_TILES, VERT_TILES
    ints = []  # TODO: Could be implemented better
    ints.append(len(PALETTE))
    for color in PALETTE:
        ints.append(color[0])
        ints.append(color[1])
        ints.append(color[2])
    ints.append(HORIZ_TILES)
    ints.append(VERT_TILES)
    for x in range(0, len(ARRAY)):
        for y in range(0, len(ARRAY[x])):
            ints.append(ARRAY[x][y])
    print(ints)
    return ints


def load_sprite_from_int_array(ints):
    global PALETTE, ARRAY, HORIZ_TILES, VERT_TILES
    print(ints)
    count = 0
    PALETTE = []
    count += 1
    for i in range(0, ints[0]):
        PALETTE.append((ints[count], ints[count + 1], ints[count + 2]))
        count += 3
    print("palette " + str(PALETTE))
    HORIZ_TILES = ints[count]
    count += 1
    VERT_TILES = ints[count]
    count += 1
    ARRAY = []
    print("horiz: " + str(HORIZ_TILES))
    print("vert: " + str(VERT_TILES))
    for x in range(0, HORIZ_TILES):
        ARRAY.append([])
        for y in range(0, VERT_TILES):
            ARRAY[x].append(ints[count])
            count += 1


def save_to_cache():
    ints_to_byte_file("cache", sprite_to_int_array())


def main():
    global PALETTE, CURRENT_COLOR, ARRAY, NEED_UPDATE, SCREEN_WIDTH, SCREEN_HEIGHT, TILE_WIDTH, IDEAL_WIDTH, IDEAL_HEIGHT, FILENAME, HORIZ_TILES, VERT_TILES, GRID, BG_COLOR, BG_COLORS
    if not os.path.exists("files/"):
        os.mkdir("files/")
    if os.path.exists("files/cache"):
        load_sprite_from_int_array(ints_from_byte_file("cache"))

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
    grid = get_grid()
    background = get_background()

    palette_display = get_palette_display(0)

    pygame.display.set_caption("Sprite Maker")
    working = True

    holding = False

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
                        for i in range(1, ints[0] + 1):
                            PALETTE.append((ints[3 * (i - 1) + 1], ints[3 * (i - 1) + 2], ints[3 * (i - 1) + 3]))
                        print("[Import Palette] Done!")
                        NEED_UPDATE = True
                    else:
                        user_in = input("[Export Palette] What is the desired filename?")
                        ints_to_byte_file(user_in, palette_to_int_array())
                        print("[Export Palette] Done!")

                if event.key == pygame.K_s:
                    if FILENAME is None:
                        user_in = input("[Save] What is the desired filename?")
                        FILENAME = user_in
                    ints_to_byte_file(FILENAME, sprite_to_int_array())
                    print("[Save] Saved as \"" + FILENAME + "\"!")

                if event.key == pygame.K_l:
                    user_in = input("[Load] What is the filename?")
                    prev_width = HORIZ_TILES
                    prev_height = VERT_TILES
                    load_sprite_from_int_array(ints_from_byte_file(user_in))
                    if prev_width == HORIZ_TILES and prev_height == VERT_TILES:
                        FILENAME = user_in
                        print("[Load] Refreshing...")
                        NEED_UPDATE = True
                    else:
                        save_to_cache()
                        raise SystemExit("[Load] Please restart!")

                if event.key == pygame.K_RIGHT:
                    CURRENT_COLOR = min(len(PALETTE) - 1, CURRENT_COLOR + 1)
                    NEED_UPDATE = True
                if event.key == pygame.K_LEFT:
                    CURRENT_COLOR = max(0, CURRENT_COLOR - 1)
                    NEED_UPDATE = True

                if event.key == pygame.K_d:
                    new_width = int(input("[Change Dimensions] What is the new width?"))
                    new_height = int(input("[Change Dimensions] What is the new height?"))
                    new_array = []
                    for x in range(0, new_width):
                        new_array.append([])
                        for y in range(0, new_height):
                            if x < HORIZ_TILES and y < VERT_TILES:
                                new_array[x].append(ARRAY[x][y])
                            else:
                                new_array[x].append(0)
                    ARRAY = new_array
                    print("array: " + str(ARRAY))
                    HORIZ_TILES = new_width
                    VERT_TILES = new_height
                    save_to_cache()
                    raise SystemExit("[Change Dimensions] Please restart!")

                if event.key == pygame.K_a:
                    new_r = int(input("[Add Color] What is the red value?"))
                    new_g = int(input("[Add Color] What is the green value?"))
                    new_b = int(input("[Add Color] What is the blue value?"))
                    PALETTE.append((new_r, new_g, new_b))
                    print("[Add Color] Added (" + str(new_r) + ", " + str(new_g) + ", " + str(new_b) + ").")
                    NEED_UPDATE = True

                if event.key == pygame.K_r:
                    color = PALETTE.pop(int(input("[Remove Color] Which index?")))
                    print("[Remove Color] Removed " + str(color) + ".")
                    NEED_UPDATE = True

                if event.key == pygame.K_c:
                    index = int(input("[Change Color] Which index?"))
                    new_r = int(input("[Change Color] What is the new red value?"))
                    new_g = int(input("[Change Color] What is the new green value?"))
                    new_b = int(input("[Change Color] What is the new blue value?"))
                    old_color = PALETTE[index]
                    PALETTE[index] = (new_r, new_g, new_b)
                    print("[Add Color] Replaced " + str(old_color) + " with " + str(PALETTE[index]) + ".")
                    NEED_UPDATE = True

                if event.key == pygame.K_g:
                    GRID = not GRID
                    NEED_UPDATE = True

                if event.key == pygame.K_b:
                    BG_COLOR = (BG_COLOR + 1) % len(BG_COLORS)
                    NEED_UPDATE = True

            if event.type == pygame.MOUSEBUTTONDOWN:
                # add ability to change selected color
                holding = True

            if event.type == pygame.MOUSEBUTTONUP:
                # add ability to change selected color
                holding = False

        if holding:
            tile = point_to_tile(pygame.mouse.get_pos())
            if 0 <= tile[0] < HORIZ_TILES and 0 <= tile[1] < VERT_TILES and not ARRAY[tile[0]][
                                                                                    tile[1]] == CURRENT_COLOR:
                ARRAY[tile[0]][tile[1]] = CURRENT_COLOR
                NEED_UPDATE = True

        if NEED_UPDATE:
            pixels = get_pixels()
            grid = get_grid()
            background = get_background()
            palette_display = get_palette_display(CURRENT_COLOR)
            NEED_UPDATE = False

        screen.blit(background, (0, 0))
        screen.blit(pixels, (0, 0))
        screen.blit(palette_display, (0, 0))
        if GRID:
            screen.blit(grid, (0, 0))
        clock.tick(60)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    main()
