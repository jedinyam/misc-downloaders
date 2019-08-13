import pixivpy3
import click
import dotenv

dotenv.load_dotenv()


class PixivDownloader(pixivpy3.AppPixivAPI):
    def __init__(self, username, password):
        self.user_info = self.login(username, password)


@click.command()
@click.argument("url")
@click.option("")
def cli(url):
    username = click.prompt("Username/Email")
    password = click.prompt("Password", hide_input=True)

    downloader = PixivDownloader(username, password)

    illust = api.illust_detail(url.split("=")[-1])
    illust_list = list()


def get_user_gallery(user_id):
    gallery = api.user_illusts(user_id)
    illust_list = list()

    for illust in illusts:
        illust_list.append(illust)

    next_qs = api.parse_qs(gallery.next_url)


if __name__ == "__main__":
    cli()
