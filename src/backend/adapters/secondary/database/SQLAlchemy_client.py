import sqlalchemy as db

from typing import Text, Dict, Any, List
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect, MetaData, event
from sqlalchemy.engine import Engine

from src.backend.adapters.secondary.database import SQLClient


@event.listens_for(Engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


class SQLAlchemyClient(SQLClient):
    def __init__(
            self, database_uri: Text = 'sqlite:///test_database', test_engine=None
    ):
        if test_engine is None:
            self._engine = db.create_engine(database_uri)
        else:
            self._engine = test_engine

    def insert_values(
            self, table: Text, values: Dict[Text, Any], **kwargs
    ) -> None:
        table_obj = db.Table(table, db.MetaData(), autoload=True, autoload_with=self._engine)
        data_obj = db.insert(table_obj).values(values)
        self._engine.connect().execute(data_obj)

    def delete_values(
            self, table: Text, cond_column_name: Text, cond_column_value: Any
    ) -> None:
        table_obj = db.Table(table, db.MetaData(), autoload=True, autoload_with=self._engine)
        data_obj = db.delete(table_obj).where(getattr(table_obj.c, cond_column_name) == cond_column_value)
        self._engine.connect().execute(data_obj)

    def update_values(
            self, table: Text, values: Dict[Text, Any], cond_column_name: Text, cond_column_value: Any
    ) -> None:
        table_obj = db.Table(table, db.MetaData(), autoload=True, autoload_with=self._engine)
        data_obj = db.update(table_obj).where(getattr(table_obj.c, cond_column_name) == cond_column_value).values(values)
        self._engine.connect().execute(data_obj)

    def get_values(
            self, table: Text, cond_column_name: Text = None, cond_column_value: Any = None
    ) -> List[Dict[Text, Any]]:
        table_obj = db.Table(table, db.MetaData(), autoload=True, autoload_with=self._engine)
        session = sessionmaker(bind=self._engine)()

        if cond_column_name and cond_column_value:
            table_values = session.query(table_obj)\
                .where(getattr(table_obj.c, cond_column_name) == cond_column_value)\
                .all()
        else:
            table_values = session.query(table_obj).all()

        session.close()
        return [
            {k: v for k, v in zip(table_obj.columns.keys(), values)}
            for values in table_values
        ]

    def get_multiple_where_values(
        self, table: Text, cond_column: Dict[Text, Any]
    ) -> List[Dict[Text, Any]]:
        table_obj = db.Table(table, db.MetaData(), autoload=True, autoload_with=self._engine)
        session = sessionmaker(bind=self._engine)()

        if len(cond_column) > 0:
            table_values = session.query(table_obj)
            for key, value in cond_column.items():
                table_values = table_values.where(getattr(table_obj.c, key) == value)
            table_values = table_values.all()
        else:
            table_values = session.query(table_obj).all()

        session.close()
        return [
            {k: v for k, v in zip(table_obj.columns.keys(), values)}
            for values in table_values
        ]

    def list_tables(self) -> List[Text]:
        inspector = inspect(self._engine)
        return list(inspector.get_table_names())

    def create_table(self, metadata: MetaData):
        metadata.create_all(self._engine)

    def query(self, query_text: Text) -> List[Dict[Any, Any]]:
        from sqlalchemy.sql import text
        values = self._engine.execute(text(query_text))
        if values.returns_rows:
            return [
                {k: v for k, v in zip(values.keys(), values)}
                for values in values
            ]
        else:
            return []


if __name__ == "__main__":
    client = SQLAlchemyClient()

    id = 17
    try:
        print((client.query("CREATE TABLE IF NOT EXISTS products ([product_id] INTEGER PRIMARY KEY, [product_name] TEXT)")))
        print(client.get_values("products", "product_id", id))
        client.insert_values("products", {"product_id": id, "product_name": "Pudim2"})
        print(client.get_values("products", "product_id", id))
        client.update_values("products", {"product_name": "Pudim3"}, "product_id", id)
        client.insert_values("products", {"product_id": id+1, "product_name": "Pudim2"})
        print(client.get_values("products", "product_id", id))
        print(client.query("SELECT * FROM products"))
        print(client.query(""))
        client.delete_values("products", "product_id", id)
        client.delete_values("products", "product_id", id+1)
        print(client.get_values("products", "product_id", id))
        print((client.query("SELECT * FROM products")))
        print((client.list_tables()))
    except Exception as ex:
        client.delete_values("products", "product_id", id)
        client.delete_values("products", "product_id", id + 1)
        raise ex


