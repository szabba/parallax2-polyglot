require 'sdl'

FOREGROUND_VEL_X = 100.0
FOREGROUND_VEL_Y = 50.0

SCREEN_W = 640
SCREEN_H = 480

TILE_W = 48
TILE_H = 48

MAP_W = 16
MAP_H = 16


class TiledLayer

    def initialize(map, tiles)
        @x = @y = 0
        @v_x = @v_y = 0
        @map = map
        @tiles = tiles
    end

    def x
        @x
    end

    def y
        @y
    end

    def set_pos(x, y)
        @x = x
        @y = y
    end

    def v_x
        @v_x
    end

    def v_y
        @v_y
    end

    def set_v(x, y)
        @v_x = x
        @v_y = y
    end

    def animate(dt)
        @x += dt * @v_x
        @y += dt * @v_y
    end

    def limit_bounce

        max_x = MAP_W * TILE_W - SCREEN_W
        max_y = MAP_H * TILE_H - SCREEN_H

        if @x >= max_x

            @v_x = -@v_x
            @x = max_x * 2 - @x

        elsif @x <= 0

            @v_x = -@v_x
            @x = -@x
        end

        if @y >= max_y

            @v_y = -@v_y
            @y = max_y * 2 - @y

        elsif @y <= 0

            @v_y = -@v_y
            @y = -@y
        end

    end

    def link(other, ratio)

        @x = other.x * ratio
        @y = other.y * ratio

    end

    def render(screen)

        map_x = (@x / TILE_W).to_i
        map_y = (@y / TILE_H).to_i

        fine_x = (@x % TILE_W).to_i
        fine_y = (@y % TILE_H).to_i

        (-fine_y).step(SCREEN_H, TILE_H) do | y |
            
            map_x_loop = map_x

            (-fine_x).step(SCREEN_W, TILE_W) do | x |

                draw_tile(
                        screen,
                        @tiles,
                        x, y,
                        @map[map_y][map_x_loop])

                map_x_loop += 1

            end

            map_y += 1

        end

    end
end


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


def draw_tile(screen, tiles, x, y, tile)

    if tile == " "
        return
    end

    SDL::Surface.blit(
            tiles,
            0, (tile.ord - "0".ord) * TILE_H,
            TILE_W, TILE_H,
            screen,
            x, y)

end


# Program body

bpp = 0
flags = 0

for arg in ARGV

    if arg == "-d"

        flags |= SDL::DOUBLEBUF

    elsif arg == "-f"

        flags |= SDL::FULLSCREEN

    else

        bpp = -arg.to_i

    end

end

SDL.init(SDL::INIT_VIDEO)

SDL.setVideoMode(SCREEN_W, SCREEN_H, bpp, flags)
screen = SDL.getVideoSurface
SDL::WM.setCaption("Parallax Scrolling Example 2", "Parallax 2")

tiles = SDL::Surface.loadBMP('tiles.bmp').display_format()

tiles.set_color_key(SDL::SRCCOLORKEY, tiles.format.map_rgb(255, 0, 255))

foreground_layer = TiledLayer.new(foreground_map, tiles)
middle_layer = TiledLayer.new(middle_map, tiles)
background_layer = TiledLayer.new(background_map, tiles)

foreground_layer.set_v(FOREGROUND_VEL_X, FOREGROUND_VEL_Y)

tick1 = SDL::getTicks()
frame_count = 0

done = false

while not done

    event = SDL::Event.poll()

    case event
    when SDL::Event::MouseButtonDown
        done = true
    end

    tick2 = SDL::getTicks()
    dt = (tick2 - tick1) * 0.001

    puts("frame: %d, dt: %d ms, fps: %.0f" % [
            frame_count,
            tick2 - tick1,
            dt > 0 ? 1.0 / dt : 0])

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

    screen.flip()

    SDL.delay(1)

end
