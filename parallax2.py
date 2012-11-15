# -*- coding: utf-8 -*-


import sys
import pygame


FOREGROUND_VEL_X = 100.0
FOREGROUND_VEL_Y = 50.0

SCREEN_W = 640
SCREEN_H = 480

TILE_W = 48
TILE_H = 48

MAP_W = 16
MAP_H = 16


class TiledLayer(object):

    def __init__(self, map, tiles):

        self.x = self.y = 0.0
        self.v_x = self.v_y = 0.0

        self.map = map
        self.tiles = tiles

    def set_pos(self, x, y):

        self.x = x
        self.y = y

    def set_v(self, x, y):

        self.v_x = x
        self.v_y = y

    def animate(self, dt):

        self.x += dt * self.v_x
        self.y += dt * self.v_y

    def limit_bounce(self):

        max_x = MAP_W * TILE_W - SCREEN_W
        max_y = MAP_H * TILE_H - SCREEN_H

        if self.x >= max_x:

            self.v_x = -self.v_x
            self.x = max_x * 2 - self.x

        elif self.x <= 0:

            self.v_x = -self.v_x
            self.x = -self.x

        if self.y >= max_y:

            self.v_y = -self.v_y
            self.y = max_y * 2 - self.y

        elif self.y <= 0:

            self.v_y = -self.v_y
            self.y = -self.y

    def link(self, other, ratio):

        self.x = other.x * ratio
        self.y = other.y * ratio

    def render(self, screen):

        map_x = int(self.x / TILE_W)
        map_y = int(self.y / TILE_H)

        fine_x = int(self.x % TILE_W)
        fine_y = int(self.y % TILE_H)

        for y in range(-fine_y, SCREEN_H, TILE_H):

            map_x_loop = map_x

            for x in range(-fine_x, SCREEN_W, TILE_W):

                draw_tile(
                        screen,
                        self.tiles,
                        x, y,
                        self.map[map_y][map_x_loop])

                map_x_loop += 1

            map_y += 1

foreground_map = [
        "3333333333333333",
        "3   2   3      3",
        "3   222 3  222 3",
        "3333 22     22 3",
        "3       222    3",
        "3   222 2 2  333",
        "3   2 2 222    3",
        "3   222      223",
        "3        333   3",
        "3  22 23 323  23",
        "3  22 32 333  23",
        "3            333",
        "3 3  22 33     3",
        "3    222  2  3 3",
        "3  3     3   3 3",
        "3333333333333333"]


middle_map = [
        "   1    1       ",
        "           1   1",
        "  1             ",
        "     1  1    1  ",
        "   1            ",
        "         1      ",
        " 1            1 ",
        "    1   1       ",
        "          1     ",
        "   1            ",
        "        1    1  ",
        " 1          1   ",
        "     1          ",
        "        1       ",
        "  1        1    ",
        "                "]


background_map = [
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000",
        "0000000000000000"]


def draw_tile(screen, tiles, x, y, tile):

    if tile == ' ':
        return

    source = (
            0,
            (ord(tile) - ord('0')) * TILE_H,
            TILE_W,
            TILE_H)

    dest = (x, y)

    screen.blit(tiles.subsurface(source), dest)


if __name__ == '__main__':

    bpp, flags = 0, 0

    pygame.init()

    for arg in sys.argv[1:]:

        if arg == '-d':
            flags |= pygame.DOUBLEBUF

        elif arg == '-f':
            flags |= pygame.FULLSCREEN

        else:
            bpp = -int(arg)

    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags, bpp)
    pygame.display.set_caption("Parallax Scrolling Example 2", "Parallax 2")

    tiles = pygame.image.load('tiles.bmp').convert()

    tiles.set_colorkey((255, 0, 255), pygame.RLEACCEL)

    foreground_layer = TiledLayer(foreground_map, tiles)
    middle_layer = TiledLayer(middle_map, tiles)
    background_layer = TiledLayer(background_map, tiles)

    foreground_layer.set_v(FOREGROUND_VEL_X, FOREGROUND_VEL_Y)

    tick1 = pygame.time.get_ticks()
    frame_count = 0

    done = False

    while not done:

        event = pygame.event.poll()

        if event.type == pygame.MOUSEBUTTONDOWN:
            done = True

        tick2 = pygame.time.get_ticks()
        dt = (tick2 - tick1) * 0.001

        print 'frame: %d, dt: %d ms, fps: %.0f\n' % (
                frame_count,
                tick2 - tick1,
                1.0 / dt if dt > 0 else 0)

        tick1 = tick2
        frame_count += 1

        foreground_layer.animate(dt)
        foreground_layer.limit_bounce()

        middle_layer.link(foreground_layer, 0.5)
        background_layer.link(foreground_layer, 0.25)

        background_layer.render(screen)
        middle_layer.render(screen)
        foreground_layer.render(screen)

        draw_tile(screen, tiles, 0, 0, '4')

        pygame.display.flip()

        pygame.time.delay(1)
