import requests
from bs4 import BeautifulSoup


class WikiCrawler:
    @staticmethod
    def __site_exist(url: str):
        request = requests.get(url)

        if request.status_code == 200:
            return True

        print("Site does not exist! [" + url + "]")
        return False

    @staticmethod
    def __get_url_to_raw(url: str):
        modified = url.replace('https://', '')
        modified = modified.replace('http://', '')

        root = modified.split('/')[0]
        title = modified.split('/')[-1]

        modified = "https://{0}/w/index.php?title={1}&action=edit".format(root, title)
        return modified

    def get_page(self, url: str):
        if not self.__site_exist(url):
            return None, None

        html_response = requests.get(url)
        html = BeautifulSoup(html_response.content, 'html.parser')
        html = html.find(id="bodyContent")
        html = html.find(id="mw-content-text")

        raw_response = requests.get(self.__get_url_to_raw(url))
        raw = BeautifulSoup(raw_response.content, 'html.parser')
        raw = raw.find(id="wpTextbox1")

        return html, raw

    def get_pages(self, urls: list):
        out = []
        for url in urls:
            out.append([self.get_page(url)])

        return out

    def get_random(self):
        request = requests.get("https://en.wikipedia.org/wiki/Special:Random")
        return self.get_page(request.url)
