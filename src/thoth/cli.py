import asyncclick as click

from thoth.pipelines.album import album_ingest


@click.group()
def main():
    pass


main.add_command(album_ingest)
