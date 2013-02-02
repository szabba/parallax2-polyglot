# -*- coding: utf-8 -*-


import pyglet
from pyglet.gl import glEnable, glBlendFunc, GL_BLEND,\
    GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA


FOREGROUND_VEL_X = 100.0
FOREGROUND_VEL_Y = 50.0

SCREEN_W = 640
SCREEN_H = 480

TILE_W = 48
TILE_H = 48

MAP_W = 16
MAP_H = 16


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


def get_tile_img(tiles, tile):

    num = ord(tile) - ord('0')

    img = tiles.get_region(
        0,
        tiles.height - (num + 1) * TILE_H,
        TILE_W,
        TILE_H)

    img.anchor_y = TILE_H

    return img


class TiledLayer(object):

    def __init__(self, map, tiles):

        self.x = self.y = 0.0
        self.v_x = self.v_y = 0.0

        self.sprites = []
        self.batch = pyglet.graphics.Batch()

        imgs = {}

        for y in range(16):

            for x in range(16):

                tile_name = map[y][x]

                if tile_name != ' ':

                    if not tile_name in imgs:

                        imgs[tile_name] = get_tile_img(tiles, tile_name)

                    tile_img = imgs[tile_name]

                    sprite = pyglet.sprite.Sprite(tile_img, batch=self.batch)

                    sprite.set_position(
                        x * TILE_W,
                        window.height - y * TILE_H)

                    self.sprites.append(sprite)

    def set_pos(self, x, y):

        dx, dy = x - self.x, y - self.y

        self.x, self.y = x, y

        for sprite in self.sprites:

            sprite.set_position(
                sprite.x + dx,
                sprite.y + dy)

    def set_v(self, x, y):

        self.v_x, self.v_y = x, y

    def draw(self):

        self.batch.draw()

    def link(self, other, ratio):

        self.set_pos(
            other.x * ratio,
            other.y * ratio)

    def animate(self, dt):

        new_x = self.x + dt * self.v_x
        new_y = self.y + dt * self.v_y

        self.set_pos(new_x, new_y)

    def limit_bounce(self):

        max_x = MAP_W * TILE_W - SCREEN_W
        max_y = MAP_H * TILE_H - SCREEN_H

        if self.x >= max_x:

            self.v_x = -self.v_x
            new_x = max_x * 2 - self.x

        elif self.x <= 0:

            self.v_x = -self.v_x
            new_x = -self.x

        else:

            new_x = self.x

        if self.y >= max_y:

            self.v_y = -self.v_y
            new_y = max_y * 2 - self.y

        elif self.y <= 0:

            self.v_y = -self.v_y
            new_y = -self.y

        else:

            new_y = self.y

        self.set_pos(new_x, new_y)

    def update(self, dt):

        self.animate(dt)
        self.limit_bounce()


if __name__ == '__main__':

    window = pyglet.window.Window(
        width=SCREEN_W,
        height=SCREEN_H,
        caption='Parallax Scrolling Example 2')

    tiles = pyglet.image.load('tiles.png')

    layers = [
        TiledLayer(foreground_map, tiles),
        TiledLayer(middle_map, tiles),
        TiledLayer(background_map, tiles)]

    fg_layer, mid_layer, bg_layer = layers

    fg_layer.set_v(FOREGROUND_VEL_X, FOREGROUND_VEL_Y)

    fps_display = pyglet.clock.ClockDisplay()

    @window.event
    def on_draw():

        window.clear()

        for layer in reversed(layers):

            layer.draw()

        fps_display.draw()

        window.flip()

    @window.event
    def on_mouse_press(x, y, button, modifiers):

        pyglet.app.exit()

    @pyglet.clock.schedule
    def update(dt):

        fg_layer.update(dt)

        mid_layer.link(fg_layer, 0.5)
        bg_layer.link(fg_layer, 0.25)

    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    pyglet.clock.set_fps_limit(60)

    pyglet.app.run()
