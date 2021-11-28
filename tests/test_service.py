import pytest
import os
import json

from fastapi.testclient import TestClient
from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import text
from dependency_injector import providers

from src.backend.start_fastapi import create_app
from src.backend.utils.db_schema_tables import create_tables
from src.backend.adapters.secondary.database.SQLAlchemy_client import SQLAlchemyClient
from src.backend.dependencies.modules import TestContainer


@pytest.fixture(scope="session")
def client():
    try:
        database_uri = 'sqlite://'
        engine = create_engine(database_uri)

        list_query = [
            "INSERT INTO users (name, email_address, academic_id, is_professor, is_admin, hashed_password) VALUES ('p1', 'e1@test.com', 'ABC_1', True, True, 'ABC');",
            "INSERT INTO users (name, email_address, academic_id, is_professor, is_admin, hashed_password) VALUES ('p2', 'e2@test.com', 'ABC_2', False, False, 'ABC');",
            "INSERT INTO users (name, email_address, academic_id, is_professor, is_admin, hashed_password) VALUES ('p3', 'e3@test.com', 'ABC_3', False, False, 'ABC');",
            "INSERT INTO projects (name, created_by) VALUES ('project_1', 1);",
            "INSERT INTO projects (name, created_by) VALUES ('project_2', 2);",
            "INSERT INTO projects (name, created_by) VALUES ('project_3', 3);",
            "INSERT INTO projects_files (name, project_id, created_by, default_code) VALUES ('projectfile_1', 1, 1, 'CODE');",
            "INSERT INTO projects_files (name, project_id, created_by, default_code) VALUES ('projectfile_2', 1, 2, 'CODE');",
            "INSERT INTO projects_files (name, project_id, created_by, default_code) VALUES ('projectfile_3', 1, 3, 'CODE');",
            "INSERT INTO testbench_files (name, projects_files_id, created_by, code) VALUES ('tb_1', 1, 1, 'code_1');",
            "INSERT INTO testbench_files (name, projects_files_id, created_by, code) VALUES ('tb_2', 1, 2, 'code_2');",
            "INSERT INTO testbench_files (name, projects_files_id, created_by, code) VALUES ('tb_3', 1, 3, 'code_3');",
            "INSERT INTO submission_files (name, project_id, metadata, code, created_by) VALUES ('projectfile_1', 1, 'meta_1', 'code_1', 1);",
            "INSERT INTO submission_files (name, project_id, metadata, code, created_by) VALUES ('projectfile_2', 1, 'meta_2', 'code_2', 2);",
            "INSERT INTO submission_files (name, project_id, metadata, code, created_by) VALUES ('projectfile_3', 1, 'meta_3', 'code_3', 3);",
        ]
        meta = create_tables()
        meta.create_all(engine)
        for query_text in list_query:
            engine.execute(text(query_text))

        os.environ["SERVICE_ENV"] = "test"

        app = create_app(True)

        app.container.database_client.override(
            providers.Factory(
                SQLAlchemyClient,
                database_uri=None,
                test_engine=engine
            )
        )
        yield TestClient(app)
    finally:
        meta.drop_all(engine)


def test_health(client):
    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.text == "true"


def test_create_user(client):
    payload = {"name": "user1", "email_address": "a.b@c.com", "academic_id": "uasdf2", "is_professor": True,
               "is_admin": True}

    response = client.post(
        "/api/create_user",
        data=json.dumps(payload)
    )
    assert response.text == "4"
    assert response.status_code == 200


def test_create_project(client):
    payload = {"name": "project1", "created_by": 1}

    response = client.post(
        "/api/create_project",
        data=json.dumps(payload)
    )
    assert response.text == "4"
    assert response.status_code == 200


def test_create_projects_files(client):
    payload = {"name": "project1", "created_by": 1, "project_id": 1, "default_code": "data code"}

    response = client.post(
        "/api/create_projects_files",
        data=json.dumps(payload)
    )
    assert response.text == "4"
    assert response.status_code == 200


def test_create_testbench_files(client):
    payload = {"name": "project1", "created_by": 1, "projects_files_id": 1, "code": ""}

    response = client.post(
        "/api/create_testbench_files",
        data=json.dumps(payload)
    )
    assert response.text == "4"
    assert response.status_code == 200


def test_create_submission_files(client):
    payload = {"name": "project1", "created_by": 1, "projects_files_id": 1, "metadata": "meta_sub", "code": "code_sub"}

    response = client.post(
        "/api/create_submission_files",
        data=json.dumps(payload)
    )
    assert response.text == "4"
    assert response.status_code == 200


def test_submit_all_codes_from_project_to_plagiarisms(client):
    response = client.get(
        "/api/submit_all_codes_from_project_to_plagiarism?project_id=1"
    )
    assert response.status_code == 200
