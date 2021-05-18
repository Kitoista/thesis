from threading import Thread, Condition

class ThreadPool:
    def __init__(self, threadJob = None, threadPoolSize = 8):
        self.threadPoolSize = threadPoolSize
        self.threadJob = threadJob
        self.inputs = None
        self.results = None

        self.threads = None
        self.threadRunnings = None
        self.mainRunnings = None
        self.steps = None
        self.running = False

        self.running = True

        self.inputs = {}
        self.results = {}

        self.threads = []
        self.threadRunnings = []
        self.mainRunnings = []
        self.step = 0
        self.steps = []

        for i in range(self.threadPoolSize):
            self.threadRunnings.append(Condition())
            self.mainRunnings.append(Condition())
            self.steps.append(0)
            self.threads.append( Thread(target=self.threadFunction, args=[i]))

    def startThreads(self):
        for i in range(self.threadPoolSize):
            self.threads[i].start()

    def nextResults(self, inputs):
        self.inputs = inputs
        for i in range(self.threadPoolSize):
            with self.threadRunnings[i]:
                self.threadRunnings[i].notify()
        for i in range(self.threadPoolSize):
            with self.mainRunnings[i]:
                if self.step >= self.steps[i]:
                    self.mainRunnings[i].wait()
        self.step += 1
        return self.results

    def killThreads(self):
        self.running = False
        for i in range(self.threadPoolSize):
            with self.threadRunnings[i]:
                self.threadRunnings[i].notify()

    def threadFunction(self, index):
        with self.threadRunnings[index]:
            self.threadRunnings[index].wait()
        while self.running:
            result = self.threadJob(self.inputs[index])

            with self.threadRunnings[index]:
                with self.mainRunnings[index]:
                    self.results[index] = result
                    self.steps[index] += 1

                    self.mainRunnings[index].notify()

                self.threadRunnings[index].wait()
