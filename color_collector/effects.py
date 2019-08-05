import abc

from typing import Iterable
from statistics import median_grouped

from .color import Color


__all__ = [
    'Effect',
]


class Effect(object, metaclass=abc.ABCMeta):
    NO_EFFECT = 'noeffect'
    NEAT_EFFECT = 'neat'
    SMOOTH_EFFECT = 'smooth'
    ACCENTUATED_EFFECT = 'accentuated'

    def __init__(self, **kwargs):
        self._wrapper = None

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

    @classmethod
    def get_effect(cls, name: str, **kwargs):
        name = name.lower().replace('-', '').replace('_', '')

        effect_class = None
        if name == cls.NO_EFFECT:
            effect_class = NoEffect
        elif name == cls.NEAT_EFFECT:
            effect_class = Neat
        elif name == cls.SMOOTH_EFFECT:
            effect_class = Smooth
        elif name == cls.ACCENTUATED_EFFECT:
            effect_class = Accentuated

        if effect_class is None:
            raise ValueError(f'No effect found {name}')

        return effect_class(**kwargs)


class NoEffect(Effect):
    pass


class Neat(Effect):

    @staticmethod
    def calc_method(items):
        return median_grouped(items)


class Smooth(Effect):

    def __init__(self, rate: int = 7, **kwargs):
        assert isinstance(rate, int)

        super().__init__(**kwargs)

        self.rate = rate
        self.history = []

    def get_colors(self, *colors: Iterable[Color]):
        self.history += colors
        return self.history[-1:-1 * len(colors) * self.rate:-1]


class Accentuated(Effect):

    def get_colors(self, *colors: Iterable[Color]):
        for color in colors:
            yield Color(*map(lambda x: (255 - x) / 255 * x + x, color))
