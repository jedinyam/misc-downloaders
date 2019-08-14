import os
from pathlib import Path
import click
try:
    import pixivpy3
except ImportError:
    pixivpy3 = None

try:
    import dotenv
    dotenv.load_dotenv()
    has_dotenv = True
except ImportError:
    has_dotenv = False


class PixivDownloader(pixivpy3.AppPixivAPI):
    def __init__(self, username, password, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_info = self.login(username, password)["response"]

    def get_user_gallery(self, *args, **kwargs):
        gallery = self.user_illusts(*args, **kwargs)
        work_list = list()

        work_list += gallery["illusts"]

        next_results = self.parse_qs(gallery["next_url"])
        if next_results:
            results = self.get_user_gallery(**next_results)
            return work_list + results
        else:
            return work_list

    @property
    def username(self):
        return self.user_info["user"]["account"]


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
            downloader.download(image["image_urls"]["large"],
                                path=str(download_directory))


if __name__ == "__main__":
    download_pixiv_gallery()
