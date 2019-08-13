import unittest
from bs4 import BeautifulSoup
from manganelo import Downloader


class ManganeloTest(unittest.TestCase):
    def setUp(self):
        self.downloader = Downloader("https://manganelo.com/manga/kimetsu_no_yaiba")

    def test_get_html(self):
        soup = self.downloader.get_html(self.downloader.url)

        self.assertIsInstance(soup, BeautifulSoup)

    def test_chapter_urls(self):
        urls = self.downloader.chapter_urls
        self.assertIsInstance(urls, map)

    def test_manga_title(self):
        title = self.downloader.manga_title
        self.assertIsInstance(title, str)
