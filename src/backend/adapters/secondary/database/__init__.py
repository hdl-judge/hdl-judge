from abc import ABC, abstractmethod
from typing import Text, Dict, Any, List


class SQLClient(ABC):
    @abstractmethod
    def __init__(self, database_uri: Text, *args, **kwargs):
        pass

    @abstractmethod
    def insert_values(self, table: Text, values: Dict[Text, Any], **kwargs) -> None:
        pass

    @abstractmethod
    def delete_values(
            self, table: Text, cond_column_name: Text, cond_column_value: Any
    ) -> None:
        pass

    @abstractmethod
    def update_values(
            self, table: Text, values: Dict[Text, Any], cond_column_name: Text, cond_column_value: Any
    ) -> None:
        pass

    @abstractmethod
    def get_values(
            self, table: Text, cond_column_name: Text = None, cond_column_value: Any = None
    ) -> List[Dict[Text, Any]]:
        pass

    @abstractmethod
    def get_multiple_where_values(
            self, table: Text, cond_column: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        pass

    @abstractmethod
    def list_tables(self) -> List[Text]:
        pass

    @abstractmethod
    def create_table(self, metadata: Any) -> List[Text]:
        pass

    @abstractmethod
    def query(self, query_text: Text) -> List[Dict[Any, Any]]:
        pass
