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

    def get_page_links(self, url: str):
        """Returns HTML & Wikicode of given site"""
        if not self.__site_exist(url):
            return None, None

        html_response = requests.get(url)
        html = BeautifulSoup(html_response.content, 'html.parser')
        html = html.find(id="bodyContent")
        html = html.find(id="mw-content-text")
        html_links = list(html.find_all('a'))

        wikicode_response = requests.get(self.__get_url_of_wikicode(url))
        wikicode = BeautifulSoup(wikicode_response.content, 'html.parser')
        wikicode_text = wikicode.find(id="wpTextbox1").get_text()
        wiki_links = self.__extract_wiki_links__(wikicode_text)

        return html_links, wiki_links

    def get_pages_links(self, urls: list):
        """Returns HTML & Wikicode of given sites"""
        out = []

        for url in urls:
            if url.split('/')[-1] == "Special:Random":
                out.append([self.get_random_page_links()])
            else:
                out.append([self.get_page_links(url)])

        return out

    def get_random_page_links(self):
        """Generates random wikipedia page and returns HTML & Wikicode of site"""
        request = requests.get("https://en.wikipedia.org/wiki/Special:Random")

        return self.get_page_links(request.url)

    def get_random_pages_links(self, count: int):
        """Generates N random wikipedia pages and returns HTML & Wikicode of sites"""
        out = []

        for i in range(count):
            out.append([self.get_random_page_links()])

        return out

    @staticmethod
    def __extract_wiki_links__(wikicode_text):
        """extract wiki links from text"""
        bracket_cnt = 0
        link = ''
        wiki_links = []
        for i in range(len(wikicode_text)):

            if wikicode_text[i] == '[' or wikicode_text[i] == '{':
                bracket_cnt += 1
                link += wikicode_text[i]
            elif wikicode_text[i] == ']'or wikicode_text[i] == '}':
                bracket_cnt -= 1
                link += wikicode_text[i]
            else:
                if link != '':
                    if bracket_cnt == 0:
                        wiki_links.append(link)
                        link = ''
                    else:
                        link += wikicode_text[i]

        return wiki_links
