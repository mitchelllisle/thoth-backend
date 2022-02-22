from base64 import urlsafe_b64encode
from typing import Any, Dict, List

import httpx
from pydantic import parse_obj_as

from thoth.config import SpotifyConfig
from thoth.datamodels import Album, AudioAnalysis, AudioFeatures, TokenResponse


class Spotify:
    def __init__(self, config: SpotifyConfig):
        self.config = config

    async def _request_headers(self) -> Dict:
        token = await self.get_token()
        return {'Authorization': f'Bearer {token.access_token.get_secret_value()}'}

    async def _make_request(
        self,
        url: str = None,
        path: str = None,
        method: str = 'GET',
        headers: Dict = None,
        data: Any = None,
        params: Any = None,
    ) -> httpx.Response:
        _url = self.config.api_url if url is None else url
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=method,
                params=params,
                url=f'{_url}{path}',
                headers=await self._request_headers() if headers is None else headers,
                data=data,
            )
        response.raise_for_status()
        return response

    async def _auth_request(self) -> httpx.Response:
        _client_values = (
            f'{self.config.client_id.get_secret_value()}'
            f':{self.config.client_secret.get_secret_value()}'
        )
        _auth_bytes = bytes(_client_values.encode())
        encoded_auth = urlsafe_b64encode(_auth_bytes)
        return await self._make_request(
            url=self.config.account_url,
            path='/api/token',
            method='POST',
            data={'grant_type': 'client_credentials'},
            headers={
                'Content-Type': 'application/x-www-form-urlencoded',
                'Authorization': f'Basic {encoded_auth.decode()}',
            },
        )

    async def get_token(self) -> TokenResponse:
        resp = await self._auth_request()
        return TokenResponse(**resp.json())

    async def album(self, album_id: str) -> Album:
        resp = await self._make_request(path=f'/albums/{album_id}')
        return Album(**resp.json())

    async def audio_features(self, track_ids: List[str]) -> List[AudioFeatures]:
        resp = await self._make_request(
            path='/audio-features/', params={'ids': ','.join(track_ids)}
        )
        items = resp.json()
        return parse_obj_as(List[AudioFeatures], items['audio_features'])

    async def audio_analysis(self, track_ids: List[str]) -> List[AudioAnalysis]:
        _analysis_results = []
        for track in track_ids:
            resp = await self._make_request(
                path=f'/audio-analysis/{track}',
            )
            data = resp.json()
            _analysis_results.append(AudioAnalysis(id=track, sections=data['sections']))
        return _analysis_results
