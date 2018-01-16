from urllib import request,parse
import sys

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()
        self.download_list = ['tv', 'korean_tv', 'china_tv', 'hongkong_tv', 'cartoon', 'jilu']

    def craw_dianyinggang(self, url):
        # 人工生成页面数
        all_pages = []
        count = 1

        for i in range(200, 481):
            if i == 1:
                all_pages.append("http://www.dygang.net/ys/index.htm")
            else:
                all_pages.append("http://www.dygang.net/ys/index_%s.htm" % i)

        for page in all_pages:
            print("spider count: %d" % count, "当前抓取的页面是 %s" % page)

            # 寻找单个页面下所有电影
            html_cout = self.downloader.download(page)
            if html_cout is None:
                continue
            page_movies = self.parser.get_movie_items(page, html_cout)

            for page_movie in page_movies.values():
                print("spider count: %d" % count, "当前抓取的页面是 %s" % page_movie['url'])
                html_cout = self.downloader.download(page_movie['url'])
                if html_cout is None:
                    continue
                item_movie_info = self.parser.get_movie_item(page_movie['url'], html_cout)
                item_movie_info['title'] = page_movie['title']
                item_movie_info['content'] = page_movie['content']
                if item_movie_info is not None:
                    self.outputer.output_html(item_movie_info)
                print("第 %d 部 当前的抓取电影是 : %s" % (count, item_movie_info['title']))
                count += 1

            if count >= 5000:
                break

    def craw_dianyinggang_tv(self, url, tv_type):
        # 人工生成页面数
        all_pages = []
        count = 1
        if tv_type not in self.download_list:
            return

        if(tv_type == 'tv'):
            for i in range(1, 152):
                if i == 1:
                    all_pages.append("http://www.dygang.net/yx/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/yx/index_%s.htm" % i)
        elif tv_type == 'korean_tv':
            for i in range(67, 80):
                if i == 1:
                    all_pages.append("http://www.dygang.net/dsj1/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/dsj1/index_%s.htm" % i)
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
            for i in range(84, 105):
                if i == 1:
                    all_pages.append("http://www.dygang.net/dmq/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/dmq/index_%s.htm" % i)
        elif tv_type == 'jilu':
            for i in range(37, 62):
                if i == 1:
                    all_pages.append("http://www.dygang.net/jilupian/index.htm")
                else:
                    all_pages.append("http://www.dygang.net/jilupian/index_%s.htm" % i)

        for page in all_pages:
            print("spider count: %d" % count, "当前抓取的页面是 %s" % page)

            # 寻找单个页面下所有电影
            html_cout = self.downloader.download(page)
            if html_cout is None:
                continue
            page_movies = self.parser.get_movie_items(page, html_cout)

            for page_movie in page_movies.values():
                print("spider count: %d" % count, "当前抓取的页面是 %s" % page_movie['url'])
                html_cout = self.downloader.download(page_movie['url'])
                if html_cout is None:
                    continue
                item_movie_info = self.parser.get_movie_item_tv(page_movie['url'], html_cout)
                item_movie_info['title'] = page_movie['title']
                item_movie_info['content'] = page_movie['content']
                #if item_movie_info is not None and tv_type == 'tv':
                #    self.outputer.output_html(item_movie_info, 'tv')
                #elif tv_type == 'korean_tv':
                self.outputer.output_html(item_movie_info, tv_type)
                print("第 %d 部 当前的抓取电视剧是 : %s" % (count, item_movie_info['title']))
                count += 1

            if count >= 2000:
                break

    def craw(self, url, craw_website):
        if craw_website == '':
            self.craw_dianyinggang(url)
        elif craw_website is not None:
            self.craw_dianyinggang_tv(url, craw_website)
        return




if __name__ == '__main__':

    root_url = "http://gaoqing.la/explosion.html"
    #电影港 高清la 美剧天堂
    craw_website = sys.argv[1]

    obj_spider = SpiderMain()
    obj_spider.craw(root_url, craw_website)
