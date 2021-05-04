import requests
from bs4 import BeautifulSoup


class WikiCrawler:
    @staticmethod
    def __site_exist(url: str):
        """Verifies if given URL is valid"""
        request = requests.get(url)

        if request.status_code == 200:
            return True

        print("Site does not exist! [" + url + "]")
        return False

    @staticmethod
    def __get_url_of_wikicode(url: str):
        """Returns URL to page containing Wikicode code"""
        wikicode_url = url.replace('https://', '')
        wikicode_url = wikicode_url.replace('http://', '')

        root = wikicode_url.split('/')[0]
        title = wikicode_url.split('/')[-1]
        wikicode_url = "https://{0}/w/index.php?title={1}&action=edit".format(root, title)

        return wikicode_url

    def get_page(self, url: str):
        """Returns HTML & Wikicode of given site"""
        if not self.__site_exist(url):
            return None, None

        html_response = requests.get(url)
        html = BeautifulSoup(html_response.content, 'html.parser')
        html = html.find(id="bodyContent")
        html = html.find(id="mw-content-text")

        wikicode_response = requests.get(self.__get_url_of_wikicode(url))
        wikicode = BeautifulSoup(wikicode_response.content, 'html.parser')
        wikicode = wikicode.find(id="wpTextbox1")

        return {"html": html, "wikicode": wikicode}

    def get_pages(self, urls: list):
        """Returns HTML & Wikicode of given sites"""
        out = []

        for url in urls:
            if url.split('/')[-1] == "Special:Random":
                out.append([self.get_random_page()])
            else:
                out.append([self.get_page(url)])

        return out

    def get_random_page(self):
        """Generates random wikipedia page and returns HTML & Wikicode of site"""
        request = requests.get("https://en.wikipedia.org/wiki/Special:Random")

        return self.get_page(request.url)

    def get_random_pages(self, count: int):
        """Generates N random wikipedia pages and returns HTML & Wikicode of sites"""
        out = []

        for i in range(count):
            out.append([self.get_random_page()])

        return out
