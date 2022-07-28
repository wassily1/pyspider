from bs4 import BeautifulSoup
from random import random
from multiprocessing import Process,Pipe
from multiprocessing import Queue
from worker import *

def master(queue,pipe):
    print('Master: Running', flush=True)
    url_seed = 'https://www.ygdy8.net/html/gndy/dyzz/list_23_'
    urlpools = []
    for i in range(1,15):
        url = url_seed+str(i)+'.html'
        urlpools.append(url)
    count = 0
    while urlpools:
        queue.put(urlpools.pop())
    queue.put(None)
    while True:
        recv = pipe.recv()
        if recv == 'All Work Done':
            break
        print("Master reveived: %s" %recv)
    pipe.close()
    print('Master: Done', flush=True)

if __name__ == '__main__':
    queue = Queue()
    masterport, workerport = Pipe()
    Master = Process(target=master, args=(queue,masterport))
    Worker1 = Process(target=worker, args=(queue,workerport,1))
    Worker2 = Process(target=worker, args=(queue,workerport,2))
    Master.start()
    Worker1.start()
    Worker2.start()
    Worker1.join()
    Worker2.join()
    Master.join()