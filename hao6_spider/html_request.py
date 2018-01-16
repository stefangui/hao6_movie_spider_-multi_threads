import requests as req
from html.parser import HTMLParser
import chardet

class HtmlRequests(object):
    def download(self, url):
        if url is None:
            return None
        headers = {
            'Accept': r'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': r'gzip, deflate',
            'Accept-Language': r'zh-CN,zh;q=0.9,en;q=0.8',
            'Cache-Control': r'max-age=0',
            'Connection': r'keep-alive',
            'Host': r'www.hao6v.com',
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36',
        }
        data = {}

        try:
            r = req.get(url, headers = headers, data = data)
            r.encoding = r.apparent_encoding

            if r.status_code != 200:
                return None

            return r.text
        except:
            return None

