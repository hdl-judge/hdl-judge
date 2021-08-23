import requests

from typing import Text


class HTTPRequests:
    def __init__(self):
        self._requests = requests

    def get(self, url: Text, **kwargs) -> requests.Response:
        return self._requests.get(url, **kwargs)