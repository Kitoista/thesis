
ImagesUpdateEvent = 1
SettingsUpdatedEvent = 2

class Event:
    def __init__(self, type, *values):
        self.type = type
        self.values = values
