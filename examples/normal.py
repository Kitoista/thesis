import time
import sys

size = int(sys.argv[1])

def threadFunction(value):
    counter = 0
    for j in range(5000000):
        counter += 1
    return value + counter

timeA = time.time()

results = {}
for i in range(size):
    results[i] = 0

for i in range(1):
    for j in range(size):
        results[j] = threadFunction(results[j])
timeB = time.time()
print(results)
print(f"{(int)((timeB - timeA) * 1000)} ms")
