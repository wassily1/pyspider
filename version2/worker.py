from crawl_msg import *


def worker(queue, pipe, id, target_url):
    print('worker %s: Running' % id, flush=True)

    while True:
        try:
            movie_dict = queue.get(timeout=3)
        except:
            break
        if not movie_dict:
            pipe.send('All Work Done')
            break
        msg = analyze_movie_info(movie_dict['detail_url'], target_url)  # 详情信息

        if msg:
            movie_dict.update(msg)

            done_info = 'worker %s job done:   ' % id
            report = done_info + str(movie_dict['movie_title'])
            pipe.send(report)
            write_msg_to_file(movie_dict)

    print('Worker %s: Done' % id, flush=True)
