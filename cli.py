import click

from misc_downloaders import (download_manganelo_manga, download_danbooru_tags,
                              download_pixiv_gallery)


@click.group()
def cli():
    pass


cli.add_command(download_manganelo_manga)

try:
    import pixivpy3  # noqa
    cli.add_command(download_pixiv_gallery)

except ImportError:
    click.echo("No pixivpy3")

try:
    import pybooru  # noqa
    cli.add_command(download_danbooru_tags)
except ImportError:
    click.echo("No booruloader")

if __name__ == "__main__":
    cli()
