
class Event:
    pass

class ImageUpdatedEvent(Event):
    pass

class SettingsUpdatedEvent(Event):
    pass

class RunningUpdatedEvent(Event):
    pass

class SaveUpdatedEvent(Event):
    pass

class OriginalUpdateEvent(Event):
    def __init__(self, original=None, originalRadon=None):
        self.original = original
        self.originalRadon = originalRadon

class ShowEvent(Event):
    def __init__(self, recon=None, reconRadon=None, step=None, error=None, cost=None, startedAt=None):
        self.recon = recon
        self.reconRadon = reconRadon
        self.step = step
        self.error = error
        self.cost = cost
        self.startedAt = startedAt
