import requests

from typing import Text

from src.backend.adapters.secondary.http import HTTPClient


class HTTPRequests(HTTPClient):
    def __init__(self):
        self._requests = requests

    def get(self, url: Text, **kwargs) -> requests.Response:
        return self._requests.get(url, **kwargs)