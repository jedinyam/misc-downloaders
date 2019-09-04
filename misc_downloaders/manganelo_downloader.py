import requests
from bs4 import BeautifulSoup


class ManganeloDownloader:
    def __init__(self, url):
        self.url = url
        try:
            self.manga_html = self.get_html(self.url)
        except requests.HTTPError:
            exit(1)

    def get_html(self, url):
        response = requests.get(url)
        response.raise_for_status()
        return BeautifulSoup(response.text, "html.parser")

    def get_last_chapter(self, chapters):
        self.chapter_urls()

    @property
    def chapter_urls(self):
        chapter_anchors = self.manga_html.find("div", {
            "class": "chapter-list"
        }).find_all("a")
        chapter_anchors.reverse()
        return map(lambda anchor: anchor["href"], chapter_anchors)

    @property
    def manga_title(self):
        return self.manga_html.find("ul", {
            "class": "manga-info-text"
        }).find("h1").text
