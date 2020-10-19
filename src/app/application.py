
class Application:
    _images = []

    @property
    def images(self):
        return self._images

    @images.setter
    def images(self, value):
        self._images = value

    # def __init__(self):
