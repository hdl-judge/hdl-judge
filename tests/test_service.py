import pytest
import os

from fastapi.testclient import TestClient

from src.backend.start_fastapi import create_app


@pytest.fixture(scope="session")
def app():
    os.environ["SERVICE_ENV"] = "test"
    app = create_app()
    return TestClient(app)


def test_pudim(app):

    response = app.get("/config")

    assert response.status_code == 200