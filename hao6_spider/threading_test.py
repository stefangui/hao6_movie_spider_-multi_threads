import threading
import time
from queue import Queue

exit_flag = 0
class myThread(threading.Thread):
    def  __init__(self, thread_id, name, q):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.q = q

    def run(self):
        print ("Starting " , self.name)
        process_data(self.name, self.q)

def process_data(thread_name, q):
    while not exit_flag:
        queue_lock.acquire()
        if not work_queue.empty():
            data = q.get()
            queue_lock.release()
            print("%s Processing Data %s \n" % (thread_name,data))
        else:
            pass
            queue_lock.release()
        time.sleep(1)
thread_list = ["thread1","thread2","thread3"]
data_list = range(50)
queue_lock = threading.Lock()
work_queue = Queue()
threads = []
thread_id = 1

queue_lock.acquire()
for data in data_list:
    work_queue.put(data)
queue_lock.release()

for t_name in thread_list:
    thread = myThread(thread_id, t_name, work_queue)
    thread.start()
    threads.append(thread)
    thread_id += 1


while not work_queue.empty():
    pass

exit_flag = 1
for t in threads:
    t.join()
    #pass

print ("exit from main thread")