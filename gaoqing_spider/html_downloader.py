from urllib import request,parse
from html.parser import HTMLParser

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36 ',
        }
        data = {}

        data = parse.urlencode(data).encode('utf-8')
        req = request.Request(url, headers=headers, data=data)
        response = request.urlopen(url)

        if response.getcode() != 200:
            return None

        return response.read().decode('utf-8')

