import time
import requests
from bs4 import BeautifulSoup

def worker(queue,pipe,id):
    print('worker %s: Running'%id, flush=True)
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36",
                }
    while True:
        try:
            url = queue.get(timeout=3)
        except:
            break
        if not url:
            pipe.send('All Work Done')
            break
        res = requests.get(url, headers = headers)
        if res.status_code!=200:
            continue
        html = res.content
        bs = BeautifulSoup(html, 'lxml')
        elements = bs.find_all('a',class_='ulink')
        result=[elements[0].get_text()]
        # for each in elements:
        #     each= each.get_text()
        #     result.append(each)
        doneinfo = 'worker %s job done:   '%id
        report = doneinfo+str(result)
        pipe.send(report)
        # print(url)
    print('Worker %s: Done'%id, flush=True)
            