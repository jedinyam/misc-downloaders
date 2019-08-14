import click

from commands.downloader_pixiv import download_pixiv_gallery
from commands.manganelo import download_manganelo_manga


@click.group()
def cli():
    pass


cli.add_command(download_pixiv_gallery)
cli.add_command(download_manganelo_manga)

if __name__ == "__main__":
    cli()