from multiprocessing import Process, Manager

threadPoolSize = 5

def nyomi(results, index):
    print(f"Working {index}")
    results[index] = index*index
    print(results)

processes = []
manager = Manager()
results = manager.dict()
for i in range(threadPoolSize):
    processes.append(Process(target=nyomi, args=(results, i, )))
    # results[i] = None
    processes[i].start()

for i in range(threadPoolSize):
    processes[i].join()

print(results)
# chosenResultIndex = 0
#
# for i in range(threadPoolSize):
#     val = results[i]
#     if newCost < cost:
#         cost = newCost
#         chosenResultIndex = i
