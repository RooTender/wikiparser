import wikicrawler

if __name__ == "__main__":
    crawler = wikicrawler.WikiCrawler()

    crawler.get_raw("https://en.wikipedia.org/wiki/Web_scraping")
