class NormalPool:
    def __init__(self, threadJob = None, threadPoolSize = 8):
        self.threadJob = threadJob
        self.threadPoolSize = threadPoolSize
        self.inputs = None
        self.results = None

    def startThreads(self):
        pass

    def nextResults(self, inputs = {}):
        self.inputs = inputs
        self.results = {}

        for i in range(self.threadPoolSize):
            self.results[i] = self.threadJob(self.inputs[i])

        return self.results

    def killThreads(self):
        pass
