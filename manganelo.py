import os
import requests
import click
from bs4 import BeautifulSoup


class Downloader:
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

    @property
    def chapter_urls(self):
        chapter_anchors = self.manga_html.find(
            "div", {"class": "chapter-list"}
        ).find_all("a")
        return map(lambda anchor: anchor["href"], chapter_anchors)

    @property
    def manga_title(self):
        return self.manga_html.find("ul", {"class": "manga-info-text"}).find("h1").text


@click.command()
@click.argument("url")
@click.option("--directory", "download_directory")
def cli(url, download_directory):
    downloader = Downloader(url)
    title = downloader.manga_title

    chapter_urls = downloader.chapter_urls

    click.echo("Downloading: " + title)

    manga_path = os.path.join(download_directory, title)
    os.makedirs(manga_path, exist_ok=True)

    for chapter_url in chapter_urls:
        image_name = chapter_url.split("/")[-1]
        chapter_dirname = os.path.join(manga_path, image_name)

        os.makedirs(chapter_dirname, exist_ok=True)

        soup = downloader.get_html(chapter_url)

        with click.progressbar(soup.find_all("img"), label=image_name) as bar:
            for image in bar:
                download_image(
                    image["src"],
                    os.path.join(chapter_dirname, image["src"].split("/")[-1]),
                )


def download_image(url, image):
    """Download image

    Args:
        url: image url
        image: file destination
    """
    with open(image, "wb") as file:
        response = requests.get(url)
        if response.status_code is requests.codes.ok:
            file.write(response.content)


if __name__ == "__main__":
    cli()
