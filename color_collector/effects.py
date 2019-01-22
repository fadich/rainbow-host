import abc

from .color import Color
from typing import Iterable, List
from statistics import median_grouped


class Effect(object, metaclass=abc.ABCMeta):
    _wrapper = None

    def get_colors(self, *colors: Iterable[Color]):
        return colors

    def __add__(self, other):
        self._wrapper = other
        return self

    def __call__(self, *colors: Iterable[Color]):
        col = Color.average(self.get_colors(*colors), self.calc_method)
        if self._wrapper:
            col = self._wrapper(col)
        return col

    @staticmethod
    def calc_method(items):
        return sum(items) / len(items)


class NoEffect(Effect):
    pass


class Neat(Effect):

    @staticmethod
    def calc_method(items):
        return median_grouped(items)


class Smooth(Effect):

    def __init__(self, rate: int = None):
        self.rate = rate
        self.history = []

    def get_colors(self, *colors: Iterable[Color]):
        if not self.rate:
            self.rate = len(colors) * 7
        self.history += colors
        return self.history[-1:-1 * self.rate:-1]


class Accentuated(Effect):

    def get_colors(self, *colors: Iterable[Color]):
        for color in colors:
            yield Color(*map(lambda x: (255 - x) / 255 * x + x, color))
