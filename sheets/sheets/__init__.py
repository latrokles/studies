import click
import ctypes
import random
import sdl2
import sys


class Color:
    def __init__(self, r, g, b, a = 255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

    @property
    def values(self):
        return [self.a, self.b, self.g, self.r]

    def to_hexstr(self):
        return hex(self.to_int())

    def to_int(self):
        c = self.r
        c <<= 8
        c += self.g
        c <<= 16
        c += self.b
        return c

    @classmethod
    def from_values(cls, values):
        alpha, blue, green, red = values
        return cls(red, green, blue, alpha)

    @classmethod
    def from_hexstr(cls, hexstr):
        color = int(hexstr, 16)
        return cls.from_int(color)

    @classmethod
    def from_int(cls, color_int):
        red = (color_int & 0xff0000) >> 16
        green = (color_int & 0xff00) >> 8
        blue  = (color_int & 0xff)
        return cls(red, green, blue)


class Palette:
    BLACK = Color.from_hexstr("000000")
    MAROON = Color.from_hexstr("800000")
    GREEN = Color.from_hexstr("008000")
    OLIVE = Color.from_hexstr("808000")
    NAVY = Color.from_hexstr("000080")
    PURPLE = Color.from_hexstr("800080")
    TEAL = Color.from_hexstr("008080")
    SILVER = Color.from_hexstr("c0c0c0")
    GREY = Color.from_hexstr("808080")
    RED = Color.from_hexstr("ff0000")
    LIME = Color.from_hexstr("00ff00")
    YELLOW = Color.from_hexstr("ffff00")
    BLUE = Color.from_hexstr("0000ff")
    FUCHSIA = Color.from_hexstr("ff00ff")
    AQUA = Color.from_hexstr("00ffff")
    WHITE = Color.from_hexstr("ffffff")
    GREY0 = Color.from_hexstr("000000")
    NAVYBLUE = Color.from_hexstr("00005f")
    DARKBLUE = Color.from_hexstr("000087")
    BLUE3 = Color.from_hexstr("0000af")
    BLUE3 = Color.from_hexstr("0000d7")
    BLUE1 = Color.from_hexstr("0000ff")
    DARKGREEN = Color.from_hexstr("005f00")
    DEEPSKYBLUE4 = Color.from_hexstr("005f5f")
    DEEPSKYBLUE4 = Color.from_hexstr("005f87")
    DEEPSKYBLUE4 = Color.from_hexstr("005faf")
    DODGERBLUE3 = Color.from_hexstr("005fd7")
    DODGERBLUE2 = Color.from_hexstr("005fff")
    GREEN4 = Color.from_hexstr("008700")
    SPRINGGREEN4 = Color.from_hexstr("00875f")
    TURQUOISE4 = Color.from_hexstr("008787")
    DEEPSKYBLUE3 = Color.from_hexstr("0087af")
    DEEPSKYBLUE3 = Color.from_hexstr("0087d7")
    DODGERBLUE1 = Color.from_hexstr("0087ff")
    GREEN3 = Color.from_hexstr("00af00")
    SPRINGGREEN3 = Color.from_hexstr("00af5f")
    DARKCYAN = Color.from_hexstr("00af87")
    LIGHTSEAGREEN = Color.from_hexstr("00afaf")
    DEEPSKYBLUE2 = Color.from_hexstr("00afd7")
    DEEPSKYBLUE1 = Color.from_hexstr("00afff")
    GREEN3 = Color.from_hexstr("00d700")
    SPRINGGREEN3 = Color.from_hexstr("00d75f")
    SPRINGGREEN2 = Color.from_hexstr("00d787")
    CYAN3 = Color.from_hexstr("00d7af")
    DARKTURQUOISE = Color.from_hexstr("00d7d7")
    TURQUOISE2 = Color.from_hexstr("00d7ff")
    GREEN1 = Color.from_hexstr("00ff00")
    SPRINGGREEN2 = Color.from_hexstr("00ff5f")
    SPRINGGREEN1 = Color.from_hexstr("00ff87")
    MEDIUMSPRINGGREEN = Color.from_hexstr("00ffaf")
    CYAN2 = Color.from_hexstr("00ffd7")
    CYAN1 = Color.from_hexstr("00ffff")
    DARKRED = Color.from_hexstr("5f0000")
    DEEPPINK4 = Color.from_hexstr("5f005f")
    PURPLE4 = Color.from_hexstr("5f0087")
    PURPLE4 = Color.from_hexstr("5f00af")
    PURPLE3 = Color.from_hexstr("5f00d7")
    BLUEVIOLET = Color.from_hexstr("5f00ff")
    ORANGE4 = Color.from_hexstr("5f5f00")
    GREY37 = Color.from_hexstr("5f5f5f")
    MEDIUMPURPLE4 = Color.from_hexstr("5f5f87")
    SLATEBLUE3 = Color.from_hexstr("5f5faf")
    SLATEBLUE3 = Color.from_hexstr("5f5fd7")
    ROYALBLUE1 = Color.from_hexstr("5f5fff")
    CHARTREUSE4 = Color.from_hexstr("5f8700")
    DARKSEAGREEN4 = Color.from_hexstr("5f875f")
    PALETURQUOISE4 = Color.from_hexstr("5f8787")
    STEELBLUE = Color.from_hexstr("5f87af")
    STEELBLUE3 = Color.from_hexstr("5f87d7")
    CORNFLOWERBLUE = Color.from_hexstr("5f87ff")
    CHARTREUSE3 = Color.from_hexstr("5faf00")
    DARKSEAGREEN4 = Color.from_hexstr("5faf5f")
    CADETBLUE = Color.from_hexstr("5faf87")
    CADETBLUE = Color.from_hexstr("5fafaf")
    SKYBLUE3 = Color.from_hexstr("5fafd7")
    STEELBLUE1 = Color.from_hexstr("5fafff")
    CHARTREUSE3 = Color.from_hexstr("5fd700")
    PALEGREEN3 = Color.from_hexstr("5fd75f")
    SEAGREEN3 = Color.from_hexstr("5fd787")
    AQUAMARINE3 = Color.from_hexstr("5fd7af")
    MEDIUMTURQUOISE = Color.from_hexstr("5fd7d7")
    STEELBLUE1 = Color.from_hexstr("5fd7ff")
    CHARTREUSE2 = Color.from_hexstr("5fff00")
    SEAGREEN2 = Color.from_hexstr("5fff5f")
    SEAGREEN1 = Color.from_hexstr("5fff87")
    SEAGREEN1 = Color.from_hexstr("5fffaf")
    AQUAMARINE1 = Color.from_hexstr("5fffd7")
    DARKSLATEGRAY2 = Color.from_hexstr("5fffff")
    DARKRED = Color.from_hexstr("870000")
    DEEPPINK4 = Color.from_hexstr("87005f")
    DARKMAGENTA = Color.from_hexstr("870087")
    DARKMAGENTA = Color.from_hexstr("8700af")
    DARKVIOLET = Color.from_hexstr("8700d7")
    PURPLE = Color.from_hexstr("8700ff")
    ORANGE4 = Color.from_hexstr("875f00")
    LIGHTPINK4 = Color.from_hexstr("875f5f")
    PLUM4 = Color.from_hexstr("875f87")
    MEDIUMPURPLE3 = Color.from_hexstr("875faf")
    MEDIUMPURPLE3 = Color.from_hexstr("875fd7")
    SLATEBLUE1 = Color.from_hexstr("875fff")
    YELLOW4 = Color.from_hexstr("878700")
    WHEAT4 = Color.from_hexstr("87875f")
    GREY53 = Color.from_hexstr("878787")
    LIGHTSLATEGREY = Color.from_hexstr("8787af")
    MEDIUMPURPLE = Color.from_hexstr("8787d7")
    LIGHTSLATEBLUE = Color.from_hexstr("8787ff")
    YELLOW4 = Color.from_hexstr("87af00")
    DARKOLIVEGREEN3 = Color.from_hexstr("87af5f")
    DARKSEAGREEN = Color.from_hexstr("87af87")
    LIGHTSKYBLUE3 = Color.from_hexstr("87afaf")
    LIGHTSKYBLUE3 = Color.from_hexstr("87afd7")
    SKYBLUE2 = Color.from_hexstr("87afff")
    CHARTREUSE2 = Color.from_hexstr("87d700")
    DARKOLIVEGREEN3 = Color.from_hexstr("87d75f")
    PALEGREEN3 = Color.from_hexstr("87d787")
    DARKSEAGREEN3 = Color.from_hexstr("87d7af")
    DARKSLATEGRAY3 = Color.from_hexstr("87d7d7")
    SKYBLUE1 = Color.from_hexstr("87d7ff")
    CHARTREUSE1 = Color.from_hexstr("87ff00")
    LIGHTGREEN = Color.from_hexstr("87ff5f")
    LIGHTGREEN = Color.from_hexstr("87ff87")
    PALEGREEN1 = Color.from_hexstr("87ffaf")
    AQUAMARINE1 = Color.from_hexstr("87ffd7")
    DARKSLATEGRAY1 = Color.from_hexstr("87ffff")
    RED3 = Color.from_hexstr("af0000")
    DEEPPINK4 = Color.from_hexstr("af005f")
    MEDIUMVIOLETRED = Color.from_hexstr("af0087")
    MAGENTA3 = Color.from_hexstr("af00af")
    DARKVIOLET = Color.from_hexstr("af00d7")
    PURPLE = Color.from_hexstr("af00ff")
    DARKORANGE3 = Color.from_hexstr("af5f00")
    INDIANRED = Color.from_hexstr("af5f5f")
    HOTPINK3 = Color.from_hexstr("af5f87")
    MEDIUMORCHID3 = Color.from_hexstr("af5faf")
    MEDIUMORCHID = Color.from_hexstr("af5fd7")
    MEDIUMPURPLE2 = Color.from_hexstr("af5fff")
    DARKGOLDENROD = Color.from_hexstr("af8700")
    LIGHTSALMON3 = Color.from_hexstr("af875f")
    ROSYBROWN = Color.from_hexstr("af8787")
    GREY63 = Color.from_hexstr("af87af")
    MEDIUMPURPLE2 = Color.from_hexstr("af87d7")
    MEDIUMPURPLE1 = Color.from_hexstr("af87ff")
    GOLD3 = Color.from_hexstr("afaf00")
    DARKKHAKI = Color.from_hexstr("afaf5f")
    NAVAJOWHITE3 = Color.from_hexstr("afaf87")
    GREY69 = Color.from_hexstr("afafaf")
    LIGHTSTEELBLUE3 = Color.from_hexstr("afafd7")
    LIGHTSTEELBLUE = Color.from_hexstr("afafff")
    YELLOW3 = Color.from_hexstr("afd700")
    DARKOLIVEGREEN3 = Color.from_hexstr("afd75f")
    DARKSEAGREEN3 = Color.from_hexstr("afd787")
    DARKSEAGREEN2 = Color.from_hexstr("afd7af")
    LIGHTCYAN3 = Color.from_hexstr("afd7d7")
    LIGHTSKYBLUE1 = Color.from_hexstr("afd7ff")
    GREENYELLOW = Color.from_hexstr("afff00")
    DARKOLIVEGREEN2 = Color.from_hexstr("afff5f")
    PALEGREEN1 = Color.from_hexstr("afff87")
    DARKSEAGREEN2 = Color.from_hexstr("afffaf")
    DARKSEAGREEN1 = Color.from_hexstr("afffd7")
    PALETURQUOISE1 = Color.from_hexstr("afffff")
    RED3 = Color.from_hexstr("d70000")
    DEEPPINK3 = Color.from_hexstr("d7005f")
    DEEPPINK3 = Color.from_hexstr("d70087")
    MAGENTA3 = Color.from_hexstr("d700af")
    MAGENTA3 = Color.from_hexstr("d700d7")
    MAGENTA2 = Color.from_hexstr("d700ff")
    DARKORANGE3 = Color.from_hexstr("d75f00")
    INDIANRED = Color.from_hexstr("d75f5f")
    HOTPINK3 = Color.from_hexstr("d75f87")
    HOTPINK2 = Color.from_hexstr("d75faf")
    ORCHID = Color.from_hexstr("d75fd7")
    MEDIUMORCHID1 = Color.from_hexstr("d75fff")
    ORANGE3 = Color.from_hexstr("d78700")
    LIGHTSALMON3 = Color.from_hexstr("d7875f")
    LIGHTPINK3 = Color.from_hexstr("d78787")
    PINK3 = Color.from_hexstr("d787af")
    PLUM3 = Color.from_hexstr("d787d7")
    VIOLET = Color.from_hexstr("d787ff")
    GOLD3 = Color.from_hexstr("d7af00")
    LIGHTGOLDENROD3 = Color.from_hexstr("d7af5f")
    TAN = Color.from_hexstr("d7af87")
    MISTYROSE3 = Color.from_hexstr("d7afaf")
    THISTLE3 = Color.from_hexstr("d7afd7")
    PLUM2 = Color.from_hexstr("d7afff")
    YELLOW3 = Color.from_hexstr("d7d700")
    KHAKI3 = Color.from_hexstr("d7d75f")
    LIGHTGOLDENROD2 = Color.from_hexstr("d7d787")
    LIGHTYELLOW3 = Color.from_hexstr("d7d7af")
    GREY84 = Color.from_hexstr("d7d7d7")
    LIGHTSTEELBLUE1 = Color.from_hexstr("d7d7ff")
    YELLOW2 = Color.from_hexstr("d7ff00")
    DARKOLIVEGREEN1 = Color.from_hexstr("d7ff5f")
    DARKOLIVEGREEN1 = Color.from_hexstr("d7ff87")
    DARKSEAGREEN1 = Color.from_hexstr("d7ffaf")
    HONEYDEW2 = Color.from_hexstr("d7ffd7")
    LIGHTCYAN1 = Color.from_hexstr("d7ffff")
    RED1 = Color.from_hexstr("ff0000")
    DEEPPINK2 = Color.from_hexstr("ff005f")
    DEEPPINK1 = Color.from_hexstr("ff0087")
    DEEPPINK1 = Color.from_hexstr("ff00af")
    MAGENTA2 = Color.from_hexstr("ff00d7")
    MAGENTA1 = Color.from_hexstr("ff00ff")
    ORANGERED1 = Color.from_hexstr("ff5f00")
    INDIANRED1 = Color.from_hexstr("ff5f5f")
    INDIANRED1 = Color.from_hexstr("ff5f87")
    HOTPINK = Color.from_hexstr("ff5faf")
    HOTPINK = Color.from_hexstr("ff5fd7")
    MEDIUMORCHID1 = Color.from_hexstr("ff5fff")
    DARKORANGE = Color.from_hexstr("ff8700")
    SALMON1 = Color.from_hexstr("ff875f")
    LIGHTCORAL = Color.from_hexstr("ff8787")
    PALEVIOLETRED1 = Color.from_hexstr("ff87af")
    ORCHID2 = Color.from_hexstr("ff87d7")
    ORCHID1 = Color.from_hexstr("ff87ff")
    ORANGE1 = Color.from_hexstr("ffaf00")
    SANDYBROWN = Color.from_hexstr("ffaf5f")
    LIGHTSALMON1 = Color.from_hexstr("ffaf87")
    LIGHTPINK1 = Color.from_hexstr("ffafaf")
    PINK1 = Color.from_hexstr("ffafd7")
    PLUM1 = Color.from_hexstr("ffafff")
    GOLD1 = Color.from_hexstr("ffd700")
    LIGHTGOLDENROD2 = Color.from_hexstr("ffd75f")
    LIGHTGOLDENROD2 = Color.from_hexstr("ffd787")
    NAVAJOWHITE1 = Color.from_hexstr("ffd7af")
    MISTYROSE1 = Color.from_hexstr("ffd7d7")
    THISTLE1 = Color.from_hexstr("ffd7ff")
    YELLOW1 = Color.from_hexstr("ffff00")
    LIGHTGOLDENROD1 = Color.from_hexstr("ffff5f")
    KHAKI1 = Color.from_hexstr("ffff87")
    WHEAT1 = Color.from_hexstr("ffffaf")
    CORNSILK1 = Color.from_hexstr("ffffd7")
    GREY100 = Color.from_hexstr("ffffff")
    GREY3 = Color.from_hexstr("080808")
    GREY7 = Color.from_hexstr("121212")
    GREY11 = Color.from_hexstr("1c1c1c")
    GREY15 = Color.from_hexstr("262626")
    GREY19 = Color.from_hexstr("303030")
    GREY23 = Color.from_hexstr("3a3a3a")
    GREY27 = Color.from_hexstr("444444")
    GREY30 = Color.from_hexstr("4e4e4e")
    GREY35 = Color.from_hexstr("585858")
    GREY39 = Color.from_hexstr("626262")
    GREY42 = Color.from_hexstr("6c6c6c")
    GREY46 = Color.from_hexstr("767676")
    GREY50 = Color.from_hexstr("808080")
    GREY54 = Color.from_hexstr("8a8a8a")
    GREY58 = Color.from_hexstr("949494")
    GREY62 = Color.from_hexstr("9e9e9e")
    GREY66 = Color.from_hexstr("a8a8a8")
    GREY70 = Color.from_hexstr("b2b2b2")
    GREY74 = Color.from_hexstr("bcbcbc")
    GREY78 = Color.from_hexstr("c6c6c6")
    GREY82 = Color.from_hexstr("d0d0d0")
    GREY85 = Color.from_hexstr("dadada")
    GREY89 = Color.from_hexstr("e4e4e4")
    GREY93 = Color.from_hexstr("eeeeee")

    @staticmethod
    def named_values():
        return {
            name: value for
            name, value in vars(Palette).items()
            if (type(value) is Color)
        }

    @staticmethod
    def values():
        return list(Palette.named_values().values())

    @staticmethod
    def random():
        return random.choice(Palette.values())


class OutOfBoundsError(Exception):
    """Raised when trying to access a location outside a form."""


class DisplayDevice:
    def __init__(self, x, y, width, height, data = None):
        self.x = x
        self.y = y
        self.w = width
        self.h = height

        if data is None:
            data = bytearray(self.w * self.h * self.depth * [0x00])
        self.fb = data

    @property
    def depth(self):
        return 4

    @property
    def offset(self):
        if self.offset_x is None and self.offset_y is None:
            return (0, 0)
        return (self.offset_x, self.offset_y)

    @property
    def bitmap_bytes(self):
        return (ctypes.c_char * len(self.fb)).from_buffer(self.fb)

    def clear(self):
        self.fb = bytearray(self.w * self.h * self.depth * [0x00])

    def color_at(self, x, y):
        x_out_of_bounds = x < 0 or self.w <= x
        y_out_of_bounds = y < 0 or self.h <= y
        if x_out_of_bounds or y_out_of_bounds:
            raise OutOfBoundsError(f'{point} is out of bounds of {self}')
        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        pixel_bytes = self.fb[_0th:_nth]
        return Color.from_values(pixel_bytes)

    def put_color_at(self, x, y, color):
        x_out_of_bounds = x < 0 or self.w <= x
        y_out_of_bounds = y < 0 or self.h <= y
        if x_out_of_bounds or y_out_of_bounds:
            return

        _0th, _nth = self._pixel_bytes_range_at_point(x, y)
        self.fb[_0th:_nth] = color.values

    def row_bytes(self, x, y, pixel_count):
        if x + (pixel_count - 1) >= self.w:
            raise OutOfBoundsError(f'reading beyond bitmap width. start={x}, pixels={pixel_count}, bitmap width={self.w}')

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + (self.depth * (pixel_count - 1))
        return self.fb[byte_0:byte_n]

    def put_row_bytes(self, x, y, row_bytes):
        if x + ((len(row_bytes) - 1) / self.depth) >= self.w:
            clip_x = (self.w - x) * self.depth
            row_bytes = row_bytes[:clip_x]

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + len(row_bytes)
        self.fb[byte_0:byte_n] = row_bytes

    def fill(self, color):
        self.fb = bytearray(self.w * self.h * color.values)

    def fill_rect(self, x, y, w, h, color):
        # naive implementation of fill_rect
        for row in range(y, y + h):
            for col in range(x, x + w):
                self.put_color_at(col, row, color)

    def _pixel_bytes_range_at_point(self, x, y):

        byte_0 = (y * (self.w * self.depth)) + (x * self.depth)
        byte_n = byte_0 + self.depth
        return byte_0, byte_n


class MouseDevice:
    """Represents an abstract mouse device, tracking
    its x and y position on the screen and its state."""

    def __init__(self):
        self.x = 0
        self.y = 0
        self.px = 0
        self.py = 0
        self.l = False
        self.m = False
        self.r = False

    @property
    def left(self):
        return self.l

    @property
    def middle(self):
        return self.m

    @property
    def right(self):
        return self.r

    def __repr__(self):
        return f'MouseDevice(x={self.x}, y={self.y}, ({self.l}, {self.m}, {self.r}))'


class Mod:
    ESC = 'ESC'
    F1 = 'F1'
    F2 = 'F2'
    F3 = 'F3'
    F4 = 'F4'
    F5 = 'F5'
    F6 = 'F6'
    F7 = 'F7'
    F8 = 'F8'
    F9 = 'F9'
    F10 = 'F10'
    F11 = 'F11'
    F12 = 'F12'
    TAB = 'TAB'
    CAPS = 'CAPS'
    LSHIFT = 'LSHIFT'
    LCTRL = 'LCTRL'
    LALT = 'LALT'
    LMETA= 'LMETA'
    SPACE = 'SPACE'
    RMETA = 'RMETA'
    RALT = 'RALT'
    RCTRL = 'RCTRL'
    RSHIFT = 'RSHIFT'
    ENTER = 'ENTER'
    DEL = 'DEL'
    BACKSPACE = 'BACKSPACE'
    UP = 'UP'
    DOWN = 'DOWN'
    LEFT = 'LEFT'
    RIGHT = 'RIGHT'


class KeyboardDevice:
    """Represents an abstract keyboard device, tracking
    the state of modifier keys as well as the text input
    key most recently pressed."""

    def __init__(self):
        self.text = ''
        self.modifiers = {
            k: 0
            for k
            in Mod.__dict__.keys()
            if not k.startswith('_')
        }

    def __str__(self):
        return f'KeyboadDevice(text={self.text}, pressed={self.pressed})'

    def down(self, modifier):
        """Set modifier key state down."""
        self.modifiers[modifier] = 1

    def up(self, modifier):
        """Set modifier key state up."""
        self.modifiers[modifier] = 0

    @property
    def pressed(self):
        """Return all pressed modifiers."""
        return {mod for mod, val in self.modifiers.items() if val == 1}

    def has_pressed(self, modifiers_to_check):
        """Return True if all modifier keys passed are pressed."""
        return all((self.modifiers[m] == 1) for m in modifiers_to_check)


class Runtime:
    """Runtime wraps all interaction with the platform's desktop
    facilities for drawing to the screen and handling input from the mouse and
    keyboard."""

    def __init__(self, width, height, scale):
        self.w = width * scale
        self.h = height * scale
        self.scale = scale
        self.screen = DisplayDevice(0, 0, width, height)
        self.draw = None

        self.mouse = MouseDevice()
        self.handle_mouse_event = None

        self.keybd = KeyboardDevice()
        self.handle_keybd_event = None

        self.running = False
        self.exiting = False

    @property
    def width_in_pixels(self):
        return self.w / self.scale

    @property
    def height_in_pixels(self):
        return self.h / self.scale

    def register_mouse_handler(self, mouse_handler):
        self.handle_mouse_event = mouse_handler

    def register_keybd_handler(self, keybd_handler):
        self.handle_keybd_event = keybd_handler

    def register_draw(self, draw):
        self.draw = draw

    def start(self):
        if sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO) < 0:
            raise RuntimeError(f'Cannot initialize SDL: {sdl2.SDL_Geterror()}')

        window_opts = sdl2.SDL_WINDOW_BORDERLESS
        self.window = sdl2.SDL_CreateWindow(
            ''.encode('utf-8'),
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            sdl2.SDL_WINDOWPOS_UNDEFINED,
            self.w,
            self.h,
            window_opts
        )

        self.renderer = sdl2.render.SDL_CreateRenderer(
            self.window,
            -1,
            sdl2.SDL_RENDERER_PRESENTVSYNC
        )

        sdl2.SDL_SetWindowMinimumSize(self.window, self.screen.w, self.screen.h)
        sdl2.render.SDL_RenderSetLogicalSize(self.renderer, self.screen.w, self.screen.h)
        sdl2.render.SDL_RenderSetIntegerScale(self.renderer, 1)

        self.texture = sdl2.SDL_CreateTexture(
            self.renderer,
            sdl2.SDL_PIXELFORMAT_RGBA8888,
            sdl2.SDL_TEXTUREACCESS_STREAMING,
            self.screen.w,
            self.screen.h,
        )
        sdl2.SDL_StartTextInput()
        self.running = True
        self.run()

    def stop(self):
        if not self.running:
            return

        self.running = False
        sdl2.SDL_StopTextInput()
        sdl2.SDL_DestroyTexture(self.texture)
        sdl2.SDL_DestroyRenderer(self.renderer)
        sdl2.SDL_DestroyWindow(self.window)
        sdl2.SDL_Quit()

    def run(self):

        while self.running:
            start = sdl2.SDL_GetPerformanceCounter()

            self._handle_events()
            if self.exiting:
                break

            self.draw(self.screen)
            self._redisplay()

            end = sdl2.SDL_GetPerformanceCounter()
            elapsed = (
                (end - start) /
                (sdl2.SDL_GetPerformanceFrequency() * 1000.0)
            )

            delay = 16.666 - elapsed
            sdl2.SDL_Delay(int(delay))
        self.stop()

    def _handle_events(self):
        event = sdl2.SDL_Event()
        while sdl2.SDL_PollEvent(event) != 0:
            handled, dev = self._handle(event)
            match handled, dev:
                case True, self.mouse:
                    self.handle_mouse_event(self.mouse)
                case True, self.keybd:
                    self.handle_keybd_event(self.keybd)
                case _, _:
                    pass

    def _redisplay(self):
        sdl2.SDL_UpdateTexture(
            self.texture,
            None,
            self.screen.bitmap_bytes,
            self.screen.w * self.screen.depth
        )
        sdl2.SDL_RenderClear(self.renderer)
        sdl2.SDL_RenderCopy(self.renderer, self.texture, None, None)
        sdl2.SDL_RenderPresent(self.renderer)

    def _handle(self, event):
        if event.type == sdl2.SDL_TEXTINPUT:
            self.keybd.text = event.text.text.decode('utf-8')
            return True, self.keybd

        if event.type == sdl2.SDL_KEYDOWN:
            key = MODS_BY_SDL_CODE.get(event.key.keysym.sym, 'text_key')
            self.keybd.down(key)
            return True, self.keybd

        if event.type == sdl2.SDL_KEYUP:
            key = MODS_BY_SDL_CODE.get(event.key.keysym.sym, 'text_key')
            self.keybd.text = ''
            self.keybd.up(key)
            return True, self.keybd

        if event.type == sdl2.SDL_MOUSEBUTTONDOWN:
            button_value = event.button.button
            match button_value:
                case 1:
                    self.mouse.l = True
                case 2:
                    self.mouse.m = True
                case 3:
                    self.mouse.r = True
                case _:
                    print(f'button_value={button_value}')
            return True, self.mouse

        if event.type == sdl2.SDL_MOUSEBUTTONUP:
            button_value = event.button.button
            match button_value:
                case 1:
                    self.mouse.l = False
                case 2:
                    self.mouse.m = False
                case 3:
                    self.mouse.r = False
                case _:
                    print(f'button_value={button_value}')
            return True, self.mouse

        if event.type == sdl2.SDL_MOUSEMOTION:
            self.mouse.px = self.mouse.x
            self.mouse.py = self.mouse.y

            self.mouse.x = event.motion.x
            self.mouse.y = event.motion.y
            return True, self.mouse

        if event.type == sdl2.SDL_QUIT:
            self.exiting = True
            return True, None

        return False, None


MODS_BY_SDL_CODE = {
    sdl2.SDLK_ESCAPE: Mod.ESC,
    sdl2.SDLK_F1: Mod.F1,
    sdl2.SDLK_F2: Mod.F2,
    sdl2.SDLK_F3: Mod.F3,
    sdl2.SDLK_F4: Mod.F4,
    sdl2.SDLK_F5: Mod.F5,
    sdl2.SDLK_F6: Mod.F6,
    sdl2.SDLK_F7: Mod.F7,
    sdl2.SDLK_F8: Mod.F8,
    sdl2.SDLK_F9: Mod.F9,
    sdl2.SDLK_F10: Mod.F10,
    sdl2.SDLK_F11: Mod.F11,
    sdl2.SDLK_F12: Mod.F12,
    sdl2.SDLK_TAB: Mod.TAB,
    sdl2.SDLK_CAPSLOCK: Mod.CAPS,
    sdl2.SDLK_LSHIFT: Mod.LSHIFT,
    sdl2.SDLK_LCTRL: Mod.LCTRL,
    sdl2.SDLK_LALT: Mod.LALT,
    sdl2.SDLK_LGUI: Mod.LMETA,
    sdl2.SDLK_SPACE: Mod.SPACE,
    sdl2.SDLK_RGUI: Mod.RMETA,
    sdl2.SDLK_RALT: Mod.RALT,
    sdl2.SDLK_RCTRL: Mod.RCTRL,
    sdl2.SDLK_RSHIFT: Mod.RSHIFT,
    sdl2.SDLK_RETURN: Mod.ENTER,
    sdl2.SDLK_DELETE: Mod.DEL,
    sdl2.SDLK_BACKSPACE: Mod.BACKSPACE,
    sdl2.SDLK_UP: Mod.UP,
    sdl2.SDLK_DOWN: Mod.DOWN,
    sdl2.SDLK_LEFT: Mod.LEFT,
    sdl2.SDLK_RIGHT: Mod.RIGHT,
}


class Window:
    def __init__(self, x, y, w, h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.color = Palette.random()

    def draw(self, screen):
        screen.fill_rect(self.x, self.y, self.w, self.h, self.color)

    def __contains__(self, coords):
        x, y = coords
        contains_x = self.x < x < self.x + self.w
        contains_y = self.y < y < self.y + self.h
        return contains_x and contains_y


class Sheets:
    def __init__(self):
        self.children = []
        self.active_window = None
        self.drag_offset_x = 0
        self.drag_offset_y = 0

    @property
    def window_count(self):
        return len(self.children)

    def create_window(self, x, y, w, h):
        self.children.append(Window(x, y, w, h))

    def on_mouse(self, mouse):
        if mouse.left:
            for i in reversed(range(0, self.window_count)):
                win = self.children[i]
                if (mouse.x, mouse.y) in win:
                    self.children.pop(i)
                    self.children.append(win)

                    self.active_window = win
                    self.drag_offset_x = mouse.x - win.x
                    self.drag_offset_y = mouse.y - win.y
                    break

        else:
            self.active_window = None
            self.drag_offset_x = 0
            self.drag_offset_y = 0

        if self.active_window is not None:
            self.active_window.x = mouse.x - self.drag_offset_x
            self.active_window.y = mouse.y - self.drag_offset_y

    def on_keybd(self, keyboard):
        if keyboard.has_pressed([Mod.ESC]):
            sys.exit(0)  # TODO fix this ugh

    def draw(self, screen):
        screen.clear()
        for win in self.children:
            win.draw(screen)
        


@click.command()
@click.option('--width', default=800, help='width')
@click.option('--height', default=600, help='height')
@click.option('--scale', default=1, help='scale')
def launch(width, height, scale):
    # I don't necessarily like this... thinking of a
    # better way to do this.

    sheets = Sheets()
    sheets.create_window(10, 10, 300, 200)
    sheets.create_window(100, 150, 400, 400)
    sheets.create_window(200, 100, 200, 300)

    runtime = Runtime(width, height, scale)
    runtime.register_mouse_handler(sheets.on_mouse)
    runtime.register_keybd_handler(sheets.on_keybd)
    runtime.register_draw(sheets.draw)

    runtime.start()


