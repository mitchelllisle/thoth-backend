import asyncclick as click
from aiostream import pipe, stream

from thoth.config import Config
from thoth.datamodels import Album
from thoth.spotify import Spotify


async def album(spotify: Spotify, album_id: str) -> Album:
    ptransform_album = stream.just(album_id) | pipe.map(spotify.album)

    album_data = await ptransform_album
    return album_data


async def features(spotify: Spotify, album_data: Album):
    ptransform_features = (
        stream.preserve(album_data) | pipe.chunks(50) | pipe.map(spotify.audio_features)
    )
    return await ptransform_features


async def analysis(spotify: Spotify, album_data: Album):
    ptransform_analysis = (
        stream.preserve(album_data) | pipe.chunks(50) | pipe.map(spotify.audio_analysis)
    )
    return await ptransform_analysis


@click.command()
@click.argument('album_id')
async def album_ingest(album_id: str):
    config = Config()
    spotify = Spotify(config.spotify)

    album_data = await album(spotify, album_id)
    await analysis(spotify, album_data)
    await features(spotify, album_data)
