from PIL import Image
from logging import Logger
from typing import Callable

from .color import Color
from .effects import Effect
from .image_grabber import ImageGrabber


class Collector(object):

    def __init__(self, image_grabber: ImageGrabber, pixel_step: int = 10,
                 zero_pixel: int = 0, logger: Logger = None):
        self._image_grabber = image_grabber
        self._pixel_step = pixel_step
        self._zero_pixel = zero_pixel
        self._logger = logger

    @property
    def image_grabber(self):
        return self._image_grabber

    @property
    def pixel_step(self):
        return self._pixel_step

    @property
    def zero_pixel(self):
        return self._zero_pixel

    def get_colors(self):
        img = next(self.image_grabber)
        x = self.zero_pixel
        while x < img.width:
            y = self.zero_pixel
            while y < img.height:
                yield Color(*img.getpixel((x, y)))
                y += self.pixel_step
            x += self.pixel_step

    def collect_color(self, effect: Effect):
        return effect(*self.get_colors())
