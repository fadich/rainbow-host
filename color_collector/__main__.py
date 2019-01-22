import sys

from typing import Iterable

from .collector import Collector
from .image_grabber import DefaultGrabber
from .effects import NoEffect, Neat, Smooth, Accentuated


def format_effects(effects: Iterable):
    def row(n, e):
        return '{:<2} {}'.format(n, e.__class__.__name__)
    return '\n'.join(row(*e) for e in enumerate(effects, 1))


def main():
    collector = Collector(DefaultGrabber())
    try:
        effects = NoEffect(), Neat(), Smooth(), Accentuated()
        enum = input('{}\nChoose effect [1]: '.format(format_effects(effects)))
        enum = int(enum) - 1 if enum.isdigit() else 0
        enum = enum if 0 <= enum <= len(effects) else 0
        effect = effects[enum]

        while True:
            print('{:<3}, {:<3}, {:<3}'.format(
                *collector.collect_color(effect)))
    except KeyboardInterrupt:
        pass

    return 0


if __name__ == '__main__':
    sys.exit(main())
