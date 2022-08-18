import pymysql


def insert(movie_id, movie_title, score, movie_cover, director, authors, actors, category, country, language,
           release_date, duration, description):
    conn = pymysql.connect(host='localhost', user='xxx', passwd='xxx', charset='utf8', db='xxx')
    cursor = conn.cursor()
    try:
        sql = "insert into movie(movie_id,movie_title,score,movie_cover,director,authors,actors,category,country,lang,release_date,duration,description) \
               values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        param = (
                    movie_id, movie_title, score, movie_cover, director, authors, actors, category, country, language,
                    release_date, duration, description)
        cursor.execute(sql, param)
        conn.commit()
    except (Exception, BaseException) as e:
        print(e)
        print("插入数据失败！")
    cursor.close()
    conn.close()


def select(cursor):
    sql = 'select * from movie'
    cursor.execute(sql)
    records = cursor.fetchall()

    for record in records:
        print(record)
    cursor.close()
    conn.close()


if __name__ == '__main__':
    conn = pymysql.connect(host='localhost', user='xxx', passwd='xxx', charset='utf8', db='xxx')
    cursor = conn.cursor()

    infile = open('details.csv', 'r', encoding='utf-8')
    data = infile.readlines()
    data = data[1:]

    for rec in data:
        record = rec.split('#')
        insert(int(record[0]), record[1], float(record[2]), record[3], record[4], record[5], record[6], record[7],
               record[8], record[9], record[10], int(record[11]), record[12])

    select(cursor)