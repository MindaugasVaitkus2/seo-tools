import bs4
import requests
import urllib


class Crawler(object):
    def __init__(self, url, depth=0):
        self.loadCache = []
        url = self.converturl(url)
        self.loadpage(url, depth)

    def islink(self, base, link):
        return link.get("href") and not link.get("href").startswith("javascript:") and urllib.parse.urlparse(urllib.parse.urljoin(base, link.get("href"))).scheme in ("http", "https")

    def ishtml(self, headers):
        return not headers.get("Content-Type") or "text/html" in headers.get("Content-Type")

    def convertlink(self, base, url):
        url = urllib.parse.urljoin(base, url)
        return self.converturl(url)

    def converturl(self, url):
        url = urllib.parse.urlparse(url)
        url = "{}://{}{}".format(url.scheme, url.netloc, url.path or "/")
        return url

    def samehost(self, a, b):
        a = urllib.parse.urlparse(a)
        b = urllib.parse.urlparse(b)
        return a.netloc == b.netloc

    def crawlpage(self, url, base, soup):
        raise NotImplementedError

    def loadpage(self, url, depth):
        if url in self.loadCache:
            return
        print("Crawling: {}".format(url))
        self.loadCache.append(url)
        try:
            request = requests.get(url)
            if request.status_code != 200:
                raise requests.exceptions.ConnectionError
        except requests.exceptions.ConnectionError:
            print("Can't load page {}".format(url))
            return
        if self.ishtml(request.headers):
            soup = bs4.BeautifulSoup(request.content, "html.parser")
            if soup.find("base") and soup.find("base").get("href"):
                base = soup.find("base").get("href")
            else:
                base = url
            self.crawlpage(url, base, soup)
            if depth > 0:
                links = soup.find_all("a")
                for link in links:
                    if self.islink(base, link):
                        href = self.convertlink(base, link.get("href"))
                        if self.samehost(url, href):
                            self.loadpage(href, depth - 1)
