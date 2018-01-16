from urllib.parse import urlparse
from urllib.parse import urljoin

from bs4 import BeautifulSoup
import re


class HtmlParser(object):
    def parse(self, page_url, html_cout):
        if page_url is None or html_cout is None:
            return

        soup = BeautifulSoup(html_cout, 'html.parser')
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        new_urls = set()

        link = soup.find('a', attrs={'rel': "prev"})

        new_url = link['href']
        #new_full_url = urljoin(page_url, new_url)
        new_urls.add(new_url)

        return new_urls
        """
        links = soup.find_all('a', rel="prev")
        for link in links:
            new_url = link['href']
            new_full_url = urlparse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls
        """

    def _get_new_data(self, page_url, soup):
        res_data = {}

        # url
        res_data['url'] = page_url

        title_node = soup.find('a', attrs={'href': re.compile(r"magnet:")})
        if title_node is None:
            res_data['href'] = "链接不存在，或者被屏蔽"
        else:
            res_data['href'] = title_node.get("href")

        summary_node = soup.find('a', attrs={'rel': "prev"})
        res_data['title'] = summary_node.get_text()

        return res_data
