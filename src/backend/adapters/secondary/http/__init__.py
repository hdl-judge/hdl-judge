from abc import ABC, abstractmethod
from typing import Any, Text


class HTTPClient(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def get(self, url: Text, **kwargs) -> Any:
        pass
