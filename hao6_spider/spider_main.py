import sys
import time
import gevent.pool
import gevent.monkey
gevent.monkey.patch_all()

import url_manager, html_downloader, html_parser, html_outputer, html_request

exit_flag = 0
count = 1

if len(sys.argv) <= 1:
    exit("no movie action!")
movie_type = sys.argv[1]

def startTimer():
    return time.time()


def ticT(startTime):
    useTime = time.time() - startTime
    return round(useTime, 3)

def gevent_process_data(url):
    global movie_type
    obj_spider = SpiderMain()
    obj_spider.craw(movie_type, url)

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
        elif tv_type == 'cartoon':
            for i in range(1, 5):
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

    def get_all_craw_url_item_url(self, tv_type):
        all_item_urls = []
        pages = self.get_all_craw_url_lists(tv_type)
        for page in pages:
            html_cout = self.downloader.download(page)
            if html_cout is None:
                return None
            page_items = self.parser.get_movie_items(page, html_cout)
            for page_item in page_items.values():
                all_item_urls.append(page_item)

        return all_item_urls


    def craw_dianyinggang_tv(self, page_movie):
        global count
        global movie_type
        tv_type = movie_type

        #print("spider count: %d" % count, "当前抓取的页面是 %s" % page_movie['url'])
        html_cout = self.downloader.download(page_movie['url'])
        if html_cout is None:
            return None
        item_movie_info = self.parser.get_movie_item_tv(page_movie['url'], html_cout)
        item_movie_info['title'] = page_movie['title']
        item_movie_info['content'] = page_movie['content']
        #if item_movie_info is not None and tv_type == 'tv':
        #    self.outputer.output_html(item_movie_info, 'tv')
        #elif tv_type == 'korean_tv':
        self.outputer.output_html(item_movie_info, tv_type)
        print("gevent协程池抓取第 %d 部 当前的抓取的 %s 是 : %s" % ( count, tv_type, item_movie_info['title']))
        count += 1

        if count >= 100000:
            return True

    def craw(self, tv_type, page):
        if page is not None:
            self.craw_dianyinggang_tv(tv_type, page)
        return

print (movie_type)

obj_spider = SpiderMain()
#放在队列里的数据
all_items = obj_spider.get_all_craw_url_item_url(movie_type)

pool = gevent.pool.Pool(30)

requestsT = startTimer()
"""
for item in all_items:
    pool.add(gevent.spawn(obj_spider.craw_dianyinggang_tv, item))
pool.join()
"""
data = pool.map(obj_spider.craw_dianyinggang_tv, all_items)
print("gevent spawn request using time: ", ticT(requestsT))

print("exit all threads\n")


