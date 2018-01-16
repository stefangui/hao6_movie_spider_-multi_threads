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

    def test(self):
        test_content = """
        <a href="#" target="_self" thunderpid="00000" thundertype="" thunderrestitle="<strong>ftp://f:f@ftp.66ys.cn:3026/[66影视www.66ys.cn]天书奇谭.rmvb</strong>" onclick="return OnDownloadClick_Simple(this,2);" oncontextmenu="ThunderNetwork_SetHref(this)" swijujlf="thunder://QUFmdHA6Ly9mOmZAZnRwLjY2eXMuY246MzAyNi9bNjYlRTUlQkQlQjElRTglQTclODZ3d3cuNjZ5cy5jbl0lRTUlQTQlQTklRTQlQjklQTYlRTUlQTUlODclRTglQjAlQUQucm12Ylpa"><strong>ftp://f:f@ftp.66ys.cn:3026/[66影视www.66ys.cn]天书奇谭.rmvb</strong></a>
        """
        soup = BeautifulSoup(test_content, 'html.parser')
        print(soup.find('a').get('swijujlf'))
        return

    def _get_new_urls(self, page_url, soup):
        new_urls = set()

        link = soup.find('a', attrs={'rel': "prev"})

        new_url = link['href']
        #new_full_url = urljoin(page_url, new_url)
        new_urls.add(new_url)

        return new_urls

    def get_movie_items(self, page_url, html_cout):
        page_movie_infos = {}

        soup = BeautifulSoup(html_cout, 'html.parser')
        links = soup.find_all('table', attrs={'width': "388"})
        counts = 0
        for link in links:
            movie_node = link.find('td', attrs={'valign': "top"})
            link_node = link.find('a', attrs={'class': "classlinkclass"})
            item_movie_url = link_node.get("href")
            movie_content = movie_node.get_text()
            movie_title = link_node.get_text()
            movie_info = {'url': item_movie_url, "content": movie_content, 'title': movie_title}
            page_movie_infos.update({counts:movie_info})
            counts += 1
        return page_movie_infos

    @staticmethod
    def get_movie_item(page_url, html_cout):
        res_data = {}

        soup = BeautifulSoup(html_cout, 'html.parser')

        # url
        res_data['url'] = page_url

        parent_node = soup.find('td', attrs={'bgcolor': "#ffffbb"})
        title_node = [];
        if parent_node is not None:
            title_node = parent_node.find('a')
        #有多个下载源
        if title_node is None:
            title_node = soup.find('a', attrs={'a': re.compile(r"magnet:")})
        #版权限制
        if title_node is None or parent_node is None:
            res_data['href'] = "链接不存在，或者被屏蔽"
        else:
            res_data['href'] = title_node.get("href")

        return res_data

    @staticmethod
    def get_movie_item_tv(page_url, html_cout):
        res_data = {}
        link_node = {}
        link_href_all = ''

        soup = BeautifulSoup(html_cout, 'html.parser')

        # url
        res_data['url'] = page_url

        parent_node = soup.find_all('td', attrs={'bgcolor': "#ffffbb"})
        parent_node_old = soup.find_all('a', attrs={'thunderpid': "00000"})
        parent_node_old2 = soup.find_all('a', attrs={'bgcolor': "#ddedfb"})
        if parent_node is not None:
            for node in parent_node:
                a_node = node.find('a')
                if a_node is None:
                    continue
                href = a_node.get('href')
                title = a_node.get_text()
                link_href_all += str(str(title) + ' : ' + str(href) + '\n')
        elif parent_node_old is not None:
            for node in parent_node:
                a_node = node
                if a_node is None:
                    continue
                href = a_node.get('hygdciaz')
                title = a_node.get_text()
                link_href_all += str(str(title) + ' : ' + str(href) + '\n')
        elif parent_node_old2 is not None:
            for node in parent_node_old2:
                a_node = node.find('a')
                if a_node is None:
                    continue
                href = a_node.get('href')
                title = a_node.get_text()
                link_href_all += str(str(title) + ' : ' + str(href) + '\n')


        if link_node is None:
            res_data['href'] = "链接不存在，或者被屏蔽"
        else:
            res_data['href'] = link_href_all

        return res_data
