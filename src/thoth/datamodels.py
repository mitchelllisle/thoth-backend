from datetime import date, datetime
from typing import List, Optional, Union

from pydantic import BaseModel, SecretStr


class TokenResponse(BaseModel):
    access_token: SecretStr
    token_type: str
    expires_in: int


class Artist(BaseModel):
    id: str
    name: str


class Track(BaseModel):
    id: str
    duration_ms: int
    explicit: bool
    name: str
    track_number: int


class Tracks(BaseModel):
    items: List[Track]


class Album(BaseModel):
    id: str
    artists: List[Artist]
    label: Optional[str]
    name: str
    release_date: Union[date, datetime]
    total_tracks: int
    tracks: Tracks

    def __iter__(self):
        yield from self.tracks.items


class AudioFeatures(BaseModel):
    id: str
    danceability: float
    energy: float
    key: int
    loudness: float
    mode: int
    speechiness: float
    acousticness: float
    instrumentalness: float
    liveness: float
    valence: float
    tempo: float
    type: str
    duration_ms: int
    time_signature: int


class Section(BaseModel):
    start: float
    duration: float
    confidence: float
    loudness: float
    tempo: float
    tempo_confidence: float
    key: int
    key_confidence: float
    mode: int
    mode_confidence: float
    time_signature: int
    time_signature_confidence: float


class AudioAnalysis(BaseModel):
    id: str
    sections: List[Section]
