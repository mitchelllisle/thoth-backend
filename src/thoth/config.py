from pydantic import BaseSettings, Field, SecretStr


class SpotifyConfig(BaseSettings):
    account_url: str = 'https://accounts.spotify.com'
    api_url: str = 'https://api.spotify.com/v1'
    client_id: SecretStr
    client_secret: SecretStr


class Config(BaseSettings):
    spotify: SpotifyConfig = Field(default_factory=SpotifyConfig)
