import requests
# import beautifulsoup4 as bs4

class WikiCrawler:
    def __site_exist(self, url):
        request = requests.get(url)

        if (request.status_code == 200):
            return True

        print("Site does not exist! [" + url + "]")
        return False

    def get_page(self, url):
        if (not self.__site_exist(url)):
            return

        

