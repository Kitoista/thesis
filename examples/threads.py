import time
from threading import Thread, Semaphore, Condition
import sys

size = int(sys.argv[1])

# def threadFunction(semaphore, nextTurn, index, inputs, results):
def threadFunction(mainRunning, threadRunning, index, inputs, results):
    with threadRunning:
        step = 0
        results[index] = (0, step)
        # print(inputs["startTime"])
        threadRunning.wait()
    while running:
        times = []
        # print(inputs["startTime"])
        times.append(time.time())
        counter = 0
        for j in range(50):
            counter += 1
            time.sleep(0.01)
        times.append(time.time())

        with threadRunning:
            with mainRunning:
                value = results[index][0]
                value += counter
                step += 1
                results[index] = (value, step)
                times.append(time.time())
                # print(f"Thread({index}): {(int)((times[1] - times[0]) * 1000)} ms base {(int)((times[2] - times[1]) * 1000)} ms end")
                # print(f"Thread({index}): {(int)((times[2] - inputs['startTime']) * 1000)} ms TOTAL")

                mainRunning.notify()

            threadRunning.wait()


timeA = time.time()

running = True

step = 0

sleepFor = 0.01
threadPoolSize = size

inputs = {
    "step": 0,
    "bonk": 0,
    # "threadRunning": Condition(),
    "startTime": 0
}
results = {}
threads = []
threadRunnings = []
mainRunnings = []
for i in range(threadPoolSize):
    threadRunnings.append(Condition())
    mainRunnings.append(Condition())
    threads.append( Thread(target=threadFunction, args=[mainRunnings[i], threadRunnings[i], i, inputs, results]))
    threads[i].start()

for step in range(10):
    times = []
    times.append(time.time())
    inputs["startTime"] = time.time()
    for i in range(threadPoolSize):

        with threadRunnings[i]:
            threadRunnings[i].notify()
    for i in range(threadPoolSize):
        with mainRunnings[i]:
            if step >= results[i][1]:
                inputs["bonk"] += 1
                mainRunnings[i].wait()

    inputs["step"] = step
    times.append(time.time())
    # print(f"Step({step}): {(int)((times[1] - times[0]) * 1000)} ms with {inputs['bonk']} bonk")

running = False

for i in range(threadPoolSize):
    with threadRunnings[i]:
        threadRunnings[i].notify()

timeB = time.time();
print(results)
print(f"{(int)((timeB - timeA) * 1000)} ms with {inputs['bonk']} bonk")
