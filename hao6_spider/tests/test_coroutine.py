import time

def consumer():
    k = ''
    while True:
        n = yield k
        if not n:
            return
        print('[CONSUMER] Consuming %s...' % n)
        time.sleep(1)
        k = '200 OK'

def produce(c):
    next(c)
    n = 0
    while n < 5:
        n = n + 1
        print('[PRODUCER] Producing %s...' % n)
        k = c.send(n)
        print('[PRODUCER] Consumer return: %s' % k)
    c.close()

if __name__=='__main__':
    c = consumer()
    produce(c)