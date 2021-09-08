from abc import ABC, abstractmethod
from typing import Text, Dict, Any


class SQLClient(ABC):
    def __init__(self, database_uri: Text, *args, **kwargs):
        pass

    @abstractmethod
    def insert_values(self, table: Text, values: Dict[Text, Any], **kwargs) -> None:
        pass
