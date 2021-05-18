from threading import Thread

class OldThreadPool:
    def __init__(self, threadJob = None, threadPoolSize = 8):
        self.threadJob = threadJob
        self.threadPoolSize = threadPoolSize
        self.inputs = None
        self.results = None
        self.threads = None

    def startThreads(self):
        pass

    def nextResults(self, inputs = {}):
        self.inputs = inputs
        self.results = {}
        self.threads = []
        for i in range(self.threadPoolSize):
            self.threads.append( Thread(target=self.threadFunction, args=[i]))
            self.threads[i].start()
        for i in range(self.threadPoolSize):
            self.threads[i].join()
        return self.results

    def killThreads(self):
        pass

    def threadFunction(self, index):
        self.results[index] = self.threadJob(self.inputs[index])
