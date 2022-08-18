from multiprocessing import Process, Pipe
from multiprocessing import Queue
from master import *
from worker import *


if __name__ == '__main__':
    url_seed = "https://movie.douban.com/"  # 目标网站
    movie_nums = 20
    target_url = url_seed + f"j/search_subjects?type=movie&tag=%E7%83%AD%E9%97%A8&page_limit={movie_nums}&page_start=0"  # 热门电影

    queue = Queue()
    master_port, worker_port = Pipe()
    Master = Process(target=master, args=(queue, master_port, url_seed, target_url))
    Worker1 = Process(target=worker, args=(queue, worker_port, 1, target_url))
    Worker2 = Process(target=worker, args=(queue, worker_port, 2, target_url))
    Master.start()
    Worker1.start()
    Worker2.start()
    Worker1.join()
    Worker2.join()
    Master.join()
