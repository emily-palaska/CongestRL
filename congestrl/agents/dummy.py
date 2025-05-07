from queue import Queue

a = Queue()
b = [1, 2, 3]
c = [4, 5, 6]
for el in b:
    a.put(el)
for el in c:
    a.put(el)
print(a.get())