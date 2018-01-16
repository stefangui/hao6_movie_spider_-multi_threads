import pymysql
import time


class HtmlOutputer(object):
    def __init__(self):
        self.datas = []
        self.conn = pymysql.connect(
            host= 'localhost',
            port= 3306,
            user= 'root',
            passwd= '',
            db= 'movie',
            use_unicode=True,
            charset="utf8",
        )

        self.cur = self.conn.cursor()
        self.cur.execute('SET NAMES utf8;')
        self.cur.execute('SET CHARACTER SET utf8;')
        self.cur.execute('SET character_set_connection=utf8;')

    def output_html(self, data):
        insert_sql = "insert into movies(movie_title,movie_download_url,movie_come_from_url,fetch_time) values('%s','%s','%s','%s')" % (data['title'], data['href'], data['url'], time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        self.cur.execute(insert_sql)

    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.append(new_data)
