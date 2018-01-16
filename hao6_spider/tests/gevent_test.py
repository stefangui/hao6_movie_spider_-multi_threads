import gevent
import random

def task(pid):
    gevent.sleep(random.randint(0,5) * 0.01)
    print("Task %s done!" % pid)

def synchronous():
    for i in range(1,6):
        task(i)

def asynchronous():
    threads = [gevent.spawn(task,i) for i in range(1,6)]
    gevent.joinall(threads)

print("synchronous: ")
synchronous()

print("asynchronous: ")
asynchronous()