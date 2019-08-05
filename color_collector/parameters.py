from collections import Iterable

from .effects import Effect


class Parameters(object):
    DEFAULT_PIXEL_STEP = 50
    DEFAULT_EFFECT = Effect.get_effect(Effect.NO_EFFECT)

    def __init__(self):
        self._parameters: dict = {}

    @property
    def effect(self) -> Effect:
        effect_list = self._parameters.get('effects', [])
        return sum(effect_list, self.DEFAULT_EFFECT)

    @effect.setter
    def effect(self, value: Iterable):
        effects = []
        for name, kwargs in value:
            effect = Effect.get_effect(name, **kwargs)
            effects.append(effect)
        self._parameters['effects'] = effects

    @property
    def pixel_step(self):
        return self._parameters.get('pixel_step', self.DEFAULT_PIXEL_STEP)

    @pixel_step.setter
    def pixel_step(self, value: int):
        assert isinstance(value, int)
        self._parameters['pixel_step'] = value
