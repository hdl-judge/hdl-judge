from logging import Logger
from typing import Optional, List, Any, Dict, Text

from src.backend.controllers import BaseController

from src.backend.adapters.secondary.http import HTTPClient


class ReadController(BaseController):
    @property
    def POSTS_ENDPOINT(self):
        return "https://www.uol.com.br/"

    def __init__(
        self,
        logger: Logger,
        http_adapter: HTTPClient
    ):
        super().__init__(logger)
        self.http_adapter = http_adapter

    def get_data(self) -> Dict[Text, Any]:

        result = self.http_adapter.get(self.POSTS_ENDPOINT)
        return result
