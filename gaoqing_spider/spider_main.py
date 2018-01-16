from urllib import request,parse

import url_manager, html_downloader, html_parser, html_outputer


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        self.outputer = html_outputer.HtmlOutputer()

    def craw(self, url):
        count = 1
        self.urls.add_new_url(url)
        while self.urls.has_new_url():
            #try:
            new_url = self.urls.get_new_url()
            print("spider count: %d" % count, "当前抓取的页面是 %s" % new_url)
            html_cout = self.downloader.download(new_url)
            new_urls, new_data = self.parser.parse(new_url, html_cout)
            self.urls.add_new_urls(new_urls)
            self.outputer.output_html(new_data)
            print("当前的抓取电影是 : %s" % new_data['title'])

            if(count >= 1500):
                    break
            count += 1
            #except:
                #print('spider failed')




if __name__ == '__main__':

    root_url = "http://gaoqing.la/a-gentleman.html"

    obj_spider = SpiderMain()
    obj_spider.craw(root_url)
