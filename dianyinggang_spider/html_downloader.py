from urllib import request,parse
from html.parser import HTMLParser
import chardet

class HtmlDownloader(object):
    def download(self, url):
        if url is None:
            return None
        headers = {
            'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36 ',
        }
        data = {}

        try:
            data = parse.urlencode(data).encode('utf-8')
            req = request.Request(url, headers=headers, data=data)
            response = request.urlopen(url)

            if response.getcode() != 200:
                return None

            repose_read = response.read()
            detectedEncodingDict = chardet.detect(repose_read)
            if detectedEncodingDict['encoding'] != "GB2312":
                return None

            return repose_read.decode('gbk')
        except:
            return None

