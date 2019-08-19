import os
from pathlib import Path

import click
from misc_downloaders.manganelo_downloader import ManganeloDownloader
from misc_downloaders.pixiv_downloader import PixivDownloader
from misc_downloaders.danbooru_downloader import DanbooruDownloader
from misc_downloaders.utils import download_image

try:
    import dotenv
    dotenv.load_dotenv()
    has_dotenv = True
except ImportError:
    has_dotenv = False


@click.command()
@click.argument("url")
@click.option("-d",
              "--directory",
              "download_directory",
              default=Path("./Downloads"))
def download_manganelo_manga(url, download_directory):
    """Download manga from the manganelo URL"""
    downloader = ManganeloDownloader(url)
    title = downloader.manga_title

    chapter_urls = downloader.chapter_urls

    click.echo("Downloading: " + title)
    manga_path = download_directory / Path(title)
    manga_path.mkdir(exist_ok=True)

    for chapter_url in chapter_urls:
        image_name = chapter_url.split("/")[-1]
        chapter_dirname = manga_path / Path(image_name)

        chapter_dirname.mkdir(exist_ok=True)

        soup = downloader.get_html(chapter_url)

        with click.progressbar(soup.find_all("img"), label=image_name) as bar:
            for image in bar:
                download_image(
                    image["src"],
                    chapter_dirname / Path(image["src"].split("/")[-1]),
                )


@click.command()
@click.argument("url")
def download_pixiv_gallery(url):

    base_directory = Path("Downloads/pixiv")
    """Download gallery from Pixiv"""

    if not has_dotenv:
        username = click.prompt("Username/Email")
        password = click.prompt("Password", hide_input=True)
    else:
        username = os.getenv("pixiv_username")
        password = os.getenv("pixiv_password")

    downloader = PixivDownloader(username, password)
    click.echo("Logged in as :" + str(downloader.username))

    work_info = downloader.illust_detail(url.split("=")[-1])

    user_gallery = downloader.get_user_gallery(
        user_id=work_info["illust"]["user"]["id"])
    download_directory = base_directory / Path(
        str(work_info["illust"]["user"]["id"]))
    download_directory.mkdir(exist_ok=True)

    with click.progressbar(user_gallery) as bar:
        for image in bar:
            bar.label = image["title"]
            if len(image["meta_pages"]):
                downloader.download(image["image_urls"]["large"],
                                    path=str(download_directory),
                                    replace=True)
            else:
                for page in image["meta_pages"]:
                    meta_path = download_directory / Path(
                        page["image_urls"]["large"])
                    downloader.download(meta_path,
                                        page["image_urls"]["large"],
                                        replace=True)


@click.command()
@click.argument("tags")
def download_danbooru_tags(tags):
    directory = Path("./Downloads/danbooru")
    downloader = DanbooruDownloader(tags)
    with click.progressbar(range(downloader.page_count),
                           label="Fetching Posts") as bar:
        posts = downloader.get_post_list(bar)

    with click.progressbar(posts, label="Downloading items") as bar:
        questionable_urls = list()
        for item in bar:
            try:
                download_image(item["large_file_url"],
                               directory / downloader.tag_path)
            except KeyError:
                try:
                    download_image(item["file_url"] / downloader.tag_path)
                except KeyError:
                    if item["source"]:
                        questionable_urls.append(item["source"])
                    else:
                        click.print(item)

    click.echo(questionable_urls)