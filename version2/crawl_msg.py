import requests
from bs4 import BeautifulSoup
import random
import re
from urllib.request import urlopen


# UA池
def get_headers(referer_url):
    first_num = random.randint(55, 76)
    third_num = random.randint(0, 3800)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_14_5)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    headers = {
        "User-Agent": ua,
        "Referer": referer_url
    }
    return headers


'''
@:return:movie_msg:包括电影详情url,电影编号，封面url,评分,电影名称,导演,编剧,主演,类型,'制片国家/地区', '语言', '上映日期', '片长',详情
'''


# 解析电影详情信息
def analyze_movie_info(detail_url, refer_url):
    keys = ['movie_id', 'movie_title', 'director', 'authors', 'actors', 'category', 'country', 'language',
            'release_date', 'duration', 'score', 'description', 'movie_cover']  # 数据库字段
    ch_keys = ['导演', '编剧', '主演', '类型', '制片国家/地区', '语言', '上映日期', '片长']  # 电影信息字段
    try:
        resp_detail = requests.get(detail_url, headers=get_headers(refer_url)).text
        main_html = BeautifulSoup(resp_detail, 'html.parser')
        msg_info = main_html.find('div', id='info')  # msg_info <=> <div>...</div>
        base_msg = msg_info.get_text().strip()  # => 就是页面中的全部内容 类型：str
        msg_list = [item.strip() for item in base_msg.split('\n') if item.strip()]  # if item.strip()去除首尾空格
        msg_single_list = [item.split(":") for item in msg_list]
        msg2 = dict(msg_single_list)

        for key in list(msg2.keys()):  # 字典在遍历时不能进行修改,因此需要转化为列表
            if key not in ch_keys:
                del msg2[key]

        msg2 = dict(zip(keys[2:10], [item.strip() for item in msg2.values()]))

        msg2['actors'] = '/'.join(msg2['actors'].split('/')[:4]).strip()  # 只取前四个演员
        msg2['duration'] = re.compile("[0-9]+", re.S).match(msg2['duration']).group()  # 去掉时长的单位，应数据库设计的要求
        msg2['release_date'] = msg2['release_date'][0:10]  # 只取一个时间

        desc = main_html.find('span', property='v:summary')  # 剧情简介
        desc = desc.get_text().strip()
        desc = desc.replace("\n", '')
        msg2['description'] = desc if len(desc) < 50 else desc[:50] + "..."

        return msg2
    except:
        # 把不符合上述规律的链接存为另一个文件中
        with open('error.csv', "a") as f:
            f.write(detail_url + "\n")
        return None


# 获取电影信息池，返回一个list，每个list里面是电影的信息
def get_dict_pool(url, target_url):
    movie_msg_pools = []

    resp = requests.get(target_url, headers=get_headers(url))
    movies_json = resp.json()  # movie_nums条电影总体数据

    for movie in movies_json['subjects']:  # movie_msg -> dict    movies_json['subjects'] -> list
        movie_msg = {'detail_url': movie['url'], 'movie_id': movie['id'], 'movie_title': movie['title'],
                     'score': movie['rate'], 'movie_cover': movie['cover']}
        # rate:评分 title:片名 url:电影详情 cover:电影封面 rate:评分 id:电影编号
        movie_msg_pools.append(movie_msg)

    return movie_msg_pools


def write_msg_to_file(movie_msg):
    # 写入电影信息数据
    with open('details.csv', 'a', encoding='utf-8') as f:
        f.writelines('#'.join(movie_msg.values()))
        f.write("\n")


def download_movie_cover(movie_msg):
    # 下载封面图片，命名格式 movie_id.jpg
    with open('imgs/' + movie_msg['movie_id'] + '.jpg', "wb") as f:
        img = urlopen(movie_msg['movie_cover']).read()
        f.write(img)
