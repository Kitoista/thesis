import time
from threading import Thread, Semaphore, Condition
import sys

size = int(sys.argv[1])

def threadFunction(index, inputs, results):
    times = []
    times.append(time.time())
    # print(f"Thread({index}): started")
    counter = 0
    for j in range(50):
        counter += 1
        time.sleep(0.01)
    times.append(time.time())

    value = results[index][0]
    value += counter
    step = results[index][1]
    step += 1
    results[index] = (value, step)
    times.append(time.time())
    # print(f"Thread({index}): {(int)((times[1] - times[0]) * 1000)} ms base {(int)((times[2] - times[1]) * 1000)} ms end")
    # print(f"Thread({index}): {(int)((times[2] - inputs['startTime']) * 1000)} ms TOTAL")


timeA = time.time()

running = True

step = 0

threadPoolSize = size

inputs = {
    "startTime": 0
}
results = {}
for i in range(threadPoolSize):
    results[i] = (0, 0)

for step in range(10):
    times = []
    times.append(time.time())
    inputs["startTime"] = time.time()
    threads = []
    for i in range(threadPoolSize):
        threads.append( Thread(target=threadFunction, args=[i, inputs, results]))
        threads[i].start()

    for i in range(threadPoolSize):
        threads[i].join()

    times.append(time.time())
    # print(f"Step({step}): {(int)((times[1] - times[0]) * 1000)} ms")

running = False

timeB = time.time();
print(results)
print(f"{(int)((timeB - timeA) * 1000)} ms")
