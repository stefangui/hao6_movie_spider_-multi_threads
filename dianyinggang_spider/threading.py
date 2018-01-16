import threading
import time

def target():
    print("the current %s threading is runing" % threading.current_threading().name )
    time.sleep(1)
    print("the current %s threading is ended" % threading.current_threading().name )

#def if __name__ == '__main__':
print("the current threading %s is running" % threading.current_threading().name)
t = threading.Thread(target = target)
t.start()
t.join()

print("the current threading %s is ended" % threading.current_threading().name )
