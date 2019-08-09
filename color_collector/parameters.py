from collections import Iterable

from .effects import Effect


class Parameters(object):
    DEFAULT_PIXEL_STEP = 50
    DEFAULT_EFFECT = Effect.get_effect(Effect.NO_EFFECT)

    def __init__(self):
        self._parameters: dict = {}

    @classmethod
    def compute_effect(cls, effect_list: Iterable):
        effects = []
        for name, kwargs in effect_list:
            effect = Effect.get_effect(name, **kwargs)
            effects.append(effect)
        return sum(effects, cls.DEFAULT_EFFECT)

    @property
    def effect(self) -> Effect:
        return self._parameters.get('effect')

    @effect.setter
    def effect(self, value: Effect):
        assert isinstance(value, Effect)
        self._parameters['effect'] = value

    @property
    def pixel_step(self):
        return self._parameters.get('pixel_step', self.DEFAULT_PIXEL_STEP)

    @pixel_step.setter
    def pixel_step(self, value: int):
        assert isinstance(value, int)
        self._parameters['pixel_step'] = value
