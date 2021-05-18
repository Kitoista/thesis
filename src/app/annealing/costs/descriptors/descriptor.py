class Descriptor:
    def __init__(self):
        self.kappa = 0.1
        pass

    def __call__(self, state):
        return 0

    def compare(self, goodValue, desc):
        return 0

    def show(self, img):
        return None
