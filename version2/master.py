from crawl_msg import *


def master(queue, pipe, url_seed, target_url):
    print('Master: Running', flush=True)

    dict_pools = get_dict_pool(url_seed, target_url)

    while dict_pools:
        queue.put(dict_pools.pop())
    queue.put(None)
    while True:
        recv = pipe.recv()
        if recv == 'All Work Done':
            break
        print("Master reveived: %s" % recv)
    pipe.close()

    print('Master: Done', flush=True)



