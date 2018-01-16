from urllib import request, parse
import sys
import threading
import time
from queue import Queue
import gevent.pool
import gevent.monkey

import url_manager, html_downloader, html_parser, html_outputer, html_request

exit_flag = 0
count = 1


class myThread(threading.Thread):
    def __init__(self, thread_id, name, q, tv_type):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name
        self.q = q
        self.tv_type = tv_type

    def run(self):
        print ("Starting ", self.name)
        process_data(self.name, self.q, self.tv_type)


def process_data(thread_name, q, tv_type):
    while not exit_flag:
        queue_lock.acquire()
        if not q.empty():
            print("start processing data using thread %s", thread_name)
            page = q.get()
            queue_lock.release()
            obj_spider = SpiderMain()
            obj_spider.craw(tv_type, page, thread_name)
        else:
            pass
            queue_lock.release()


def gevent_process_data(tv_type, url):


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_request.HtmlRequests()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.download_list = ['gq_movie', 'hao6_mj', 'china_tv', 'hongkong_tv', 'cartoon', 'jilu']

    def get_all_craw_url_lists(self, tv_type):
        all_pages = []
        if tv_type not in self.download_list:
            return

        if (tv_type == 'gq_movie'):
            for i in range(1, 318):
                if i == 1:
                    all_pages.append("http://www.hao6v.com/gq/index.html")
                else:
                    all_pages.append("http://www.hao6v.com/gq/index_%s.html" % i)
        elif tv_type == 'hao6_mj':
            for i in range(2, 49):
                if i == 1:
                    all_pages.append("http://www.hao6v.com/mj/")
                else:
                    all_pages.append("http://www.hao6v.com/mj/index_%s.html" % i)
        elif tv_type == 'china_tv':
            for i in range(1, 210):
                if i == 1:
                    all_pages.append("http://www.dygang.net/dsj/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/dsj/index_%s.htm" % i)
        elif tv_type == 'hongkong_tv':
            for i in range(1, 90):
                if i == 1:
                    all_pages.append("http://www.dygang.net/gp/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/gp/index_%s.htm" % i)
        elif tv_type == 'cartoon':
            for i in range(1, 84):
                if i == 1:
                    all_pages.append("http://www.hao6v.com/jddy/index.html")
                else:
                    all_pages.append("http://www.hao6v.com/jddy/index_%s.html" % i)
        elif tv_type == 'jilu':
            for i in range(37, 62):
                if i == 1:
                    all_pages.append("http://www.dygang.net/jilupian/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/jilupian/index_%s.htm" % i)
        return all_pages

    def craw_dianyinggang_tv(self, tv_type, page, thread_name):
        global count
        # 人工生成页面数
        # for page in all_pages:
        # print("spider count: %d" % count, "当前抓取的页面是 %s" % page)

        # 寻找单个页面下所有电影
        html_cout = self.downloader.download(page)

        if html_cout is None:
            return None

        page_movies = self.parser.get_movie_items(page, html_cout)

        for page_movie in page_movies.values():
            # print("spider count: %d" % count, "当前抓取的页面是 %s" % page_movie['url'])
            html_cout = self.downloader.download(page_movie['url'])
            if html_cout is None:
                continue
            item_movie_info = self.parser.get_movie_item_tv(page_movie['url'], html_cout)
            item_movie_info['title'] = page_movie['title']
            item_movie_info['content'] = page_movie['content']
            # if item_movie_info is not None and tv_type == 'tv':
            #    self.outputer.output_html(item_movie_info, 'tv')
            # elif tv_type == 'korean_tv':
            self.outputer.output_html(item_movie_info, tv_type)
            print("线程 %s 抓取第 %d 部 当前的抓取的 %s 是 : %s" % (thread_name, count, tv_type, item_movie_info['title']))
            count += 1

        if count >= 100000:
            return True

    def craw(self, tv_type, page, thread_name):
        if page is not None:
            self.craw_dianyinggang_tv(tv_type, page, thread_name)
        return


if sys.argv[1] == None:
    exit("no movie action!")
movie_type = sys.argv[1]

print (movie_type)
if movie_type is None:
    exit("no movie type!")

obj_spider = SpiderMain()
# 开启三个线程
thread_list = ["thread1", "thread2", "thread3", "thread4", "thread5"]
# 放在队列里的数据
data_list = obj_spider.get_all_craw_url_lists(movie_type)

pool = gevent.pool.Pool(20)
data = pool.map(download_requests, data_list)

queue_lock = threading.Lock()
work_queue = Queue()
threads = []
thread_id = 1

queue_lock.acquire()
for page in data_list:
    work_queue.put(page)
queue_lock.release()

for thread in thread_list:
    thread = myThread(thread_id, thread, work_queue, movie_type)
    thread.start()
    threads.append(thread)
    thread_id += 1

while not work_queue.empty():
    pass

exit_flag = 1
for thread in threads:
    thread.join()

print("exit all threads\n")


