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

    def output_html(self, data, movietype='movie'):
        title = pymysql.escape_string(data['title'])
        content = pymysql.escape_string(data['content'])
        href = pymysql.escape_string(data['href'])
        insert_sql = "insert into movies_new(movie_title, movie_content, movie_download_url, movie_come_from_url,movie_type,fetch_time) values('%s','%s','%s','%s','%s','%s')" % (title, content, href, data['url'], movietype, time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
        #print(insert_sql)
        self.cur.execute(insert_sql)

    def collect_data(self, new_data):
        if new_data is None:
            return
        self.datas.append(new_data)
