from typing import Iterable, Callable


class Color(object):

    def __init__(self, red: int, green: int, blue: int):
        self._rgb = red, green, blue

    def __int__(self):
        return sum([v << 8 * k for k, v in enumerate(self._rgb[::-1])])

    def __iter__(self):
        for val in self._rgb:
            yield val

    @property
    def hex_code(self):
        return '#{:06X}'.format(int(self))

    @staticmethod
    def from_int(color: int):
        return Color((color >> 16) & 255, (color >> 8) & 255, color & 255)

    @staticmethod
    def average(colors: Iterable, calc_method: Callable):
        # Average values
        r, g, b = (int(calc_method(color)) for color in zip(*colors))
        return Color(r, g, b)


if __name__ == '__main__':
    print(Color(0, 0, 0).hex_code)
