from . import crawler


class BrokenLinkCrawler(crawler.Crawler):
    def __init__(self, url, depth=0):
        self.linkCache = []
        self.requestCache = {}
        super().__init__(url, depth)

    def crawlpage(self, url, base, soup):
        links = soup.find_all("a")
        for link in links:
            if self.islink(base, link):
                if str(link) in self.linkCache:
                    continue
                self.linkCache.append(str(link))
                href = self.convertlink(base, link.get("href"))
                if href in self.requestCache.keys():
                    if self.requestCache[href] == False:
                        print("BROKEN: {}".format(link))
                else:
                    try:
                        request = crawler.requests.get(href)
                        if request.status_code != 200:
                            raise crawler.requests.exceptions.ConnectionError
                    except crawler.requests.exceptions.ConnectionError:
                        self.requestCache[href] = False
                        print("BROKEN: {}".format(link))
                    else:
                        self.requestCache[href] = True
