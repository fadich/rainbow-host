import tkinter as tk

from threading import Thread, Event
from logging import getLogger, DEBUG, basicConfig, ERROR

from color_collector.collector import Collector
from color_collector.image_grabber import DefaultGrabber
from color_collector.effects import NoEffect, Neat, Smooth, Accentuated


def read_color(canvas: tk.Canvas, break_event: Event):
    logger.info('Loading read color...')

    effect = Neat() + Accentuated() + Smooth()
    grabber = DefaultGrabber()
    collector = Collector(grabber, pixel_step=50)
    while not break_event.is_set():
        logger.debug('Reading color...')
        average = collector.collect_color(effect)
        logger.debug('Average: ({}, {}, {})'.format(*average))
        canvas.config(bg=average.hex_code)


if __name__ == '__main__':
    logger = getLogger('Main')
    basicConfig(level=ERROR)

    root = tk.Tk()
    root.wm_attributes('-topmost', 1)
    # root.wm_attributes('-disabled', True)
    root.resizable(0, 0)
    root.geometry('120x80')
    root.geometry('+0+0')
    root.title('Rainbow')
    root.protocol('WM_DELETE_WINDOW', lambda: 0)

    cv = tk.Canvas(name='img')
    cv.config(bg='#000000')
    cv.pack(side='top', fill='both', expand='yes')
    event = Event()
    thread = Thread(target=read_color, daemon=True, args=(cv, event, ))
    thread.start()

    try:
        print('Press [Ctrl+C] to exit...')
        root.mainloop()
    except KeyboardInterrupt:
        pass
    finally:
        logger.info('Closing...')
        event.set()
        logger.info('Event is set...')
        thread.join()
        logger.info('Thread {} joined'.format(thread.name))
