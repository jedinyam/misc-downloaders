import click

from misc_downloaders import download_pixiv_gallery, download_manganelo_manga


@click.group()
def cli():
    pass


cli.add_command(download_pixiv_gallery)
try:
    import pixivpy3  # noqa
    cli.add_command(download_manganelo_manga)
except ImportError:
    click.echo("No pixivpy3")

if __name__ == "__main__":
    cli()
