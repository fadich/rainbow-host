import abc

from PIL import ImageGrab


class ImageGrabber(object, metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def __next__(self):
        pass

    def __iter__(self):
        return self


class DefaultGrabber(ImageGrabber):

    def __next__(self):
        return ImageGrab.grab()
