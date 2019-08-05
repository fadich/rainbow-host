from typing import Union

from time import sleep
from queue import Queue as TQueue
from threading import Event as TEvent
from logging import getLogger, Logger
from multiprocessing import Queue as PQueue, Event as PEvent

from .collector import Collector
from .parameters import Parameters
from .image_grabber import ImageGrabber, DefaultGrabber


__all__ = [
    'grab_color',
]


def grab_color(result_queue: Union[TQueue, PQueue], params: Parameters = None,
               break_event: Union[TEvent, PEvent] = None, logger: Logger = None,
               grabber: ImageGrabber = None, delay: float = 0.001):
    """Calculate image average color.

    :param result_queue: The results stream queue
    :param params: Behaviour params
    :param break_event: A mutex event
    :param logger: Specific logger
    :param grabber: Image provider iterator
    :param delay: The pause between iterations
    """

    assert delay > 0
    logger = logger or getLogger(__name__)
    grabber = grabber or DefaultGrabber()
    color_collector = Collector(grabber, pixel_step=params.pixel_step)

    while not (break_event and break_event.is_set()):
        avg_color = color_collector.collect_color(params.effect)
        result_queue.put(avg_color)
        logger.debug('Average: ({}, {}, {})'.format(*avg_color))

        sleep(delay)
