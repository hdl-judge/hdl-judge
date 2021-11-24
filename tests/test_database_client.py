import pytest
from sqlalchemy import create_engine
import sqlalchemy as db
from sqlalchemy.sql import text
from sqlalchemy import inspect, MetaData
from sqlalchemy import MetaData, Table, Column, Integer, String

from src.backend.utils.db_schema_tables import create_tables
from src.backend.adapters.secondary.database.SQLAlchemy_client import SQLAlchemyClient


@pytest.fixture(scope="function")
def setup_database():
    database_uri = 'sqlite://'
    engine = create_engine(database_uri)

    list_query = [
        "INSERT INTO users (name, email_address, academic_id, is_professor, is_admin, hashed_password) VALUES ('p1', 'e1@test.com', 'ABC_1', True, True, 'TESTE1');",
        "INSERT INTO users (name, email_address, academic_id, is_professor, is_admin, hashed_password) VALUES ('p2', 'e2@test.com', 'ABC_2', False, False, 'TESTE2');",
        "INSERT INTO users (name, email_address, academic_id, is_professor, is_admin, hashed_password) VALUES ('p3', 'e3@test.com', 'ABC_3', False, False, 'TESTE3');",
    ]
    create_tables().create_all(engine)
    for query_text in list_query:
        engine.execute(text(query_text))

    yield SQLAlchemyClient(test_engine=engine), engine
    create_tables().drop_all(engine)


def test_insert_values_base(setup_database):
    client, engine = setup_database
    name = "Nome Pessoa"
    email_address = "email@email.com"
    academic_id = "ACD123"
    is_professor = True
    is_admin = False
    hashed_password = "TESTE"
    values = {
        "name": name,
        "email_address": email_address,
        "academic_id": academic_id,
        "is_professor": is_professor,
        "is_admin": is_admin,
        "hashed_password": hashed_password
    }
    client.insert_values("users", values)
    expected = [(4, name, email_address, academic_id, is_professor, is_admin, hashed_password)]
    result = engine.execute(text(f"SELECT * FROM users WHERE name='{name}'"))
    assert list(result) == expected


def test_delete_values_base(setup_database):
    client, engine = setup_database
    result_b = engine.execute(text(f"SELECT * FROM users WHERE id=1"))
    client.delete_values("users", "id", 1)
    expected = [(1, 'p1', 'e1@test.com', 'ABC_1', True, True, 'TESTE1')]
    result_a = engine.execute(text(f"SELECT * FROM users WHERE id=1"))
    assert list(result_b) == expected
    assert list(result_a) == []


def test_update_values_base(setup_database):
    client, engine = setup_database
    expected_b = [(1, 'p1', 'e1@test.com', 'ABC_1', True, True, 'TESTE1')]
    result_b = engine.execute(text(f"SELECT * FROM users WHERE id=1"))
    client.update_values("users", {"name": "p_change"}, "id", 1)
    expected_a = [(1, 'p_change', 'e1@test.com', 'ABC_1', True, True, 'TESTE1')]
    result_a = engine.execute(text(f"SELECT * FROM users WHERE id=1"))
    assert list(result_b) == expected_b
    assert list(result_a) == expected_a


def test_list_tables(setup_database):
    client, engine = setup_database
    expected = ['projects', 'projects_files', 'submission_files', 'testbench_files', 'users']
    result = client.list_tables()
    assert expected == result


def test_create_tables(setup_database):
    client, engine = setup_database
    expected_b = ['projects', 'projects_files', 'submission_files', 'testbench_files', 'users']
    result_b = list(inspect(engine).get_table_names())

    meta = MetaData()
    user = Table(
        'testTable', meta,
        Column('id', Integer, primary_key=True, autoincrement=True),
        Column('name', String),
    )
    meta.create_all(engine)
    expected_a = ['projects', 'projects_files', 'submission_files', 'testTable', 'testbench_files', 'users']
    result_a = list(inspect(engine).get_table_names())

    assert result_b == expected_b
    assert result_a == expected_a

