import sys

from time import sleep
from queue import Queue
from threading import Thread, Event
# from multiprocessing import Process, Event, Queue

from color_collector import grab_color
from color_collector.effects import Effect
from color_collector.parameters import Parameters


def main():
    event = Event()
    results = Queue()
    params = Parameters()
    params.pixel_step = 25
    params.effect = (
        (Effect.NEAT_EFFECT, {}),
        (Effect.ACCENTUATED_EFFECT, {}),
        (Effect.ACCENTUATED_EFFECT, {}),
        (Effect.SMOOTH_EFFECT, {'rate': 7}),
    )

    kwargs = {
        'params': params,
        'break_event': event,
        'result_queue': results,
        # 'delay': 0.5,
    }

    proc = Thread(target=grab_color, kwargs=kwargs)
    proc.start()

    try:
        while True:
            sleep(0.001)
            if results.empty():
                continue
            color = results.get()
            print('{:<3}, {:<3}, {:<3}'.format(*color))
    except KeyboardInterrupt:
        pass
    finally:
        event.set()
        proc.join()

    return 0


if __name__ == '__main__':
    sys.exit(main())
