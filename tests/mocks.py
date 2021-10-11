import pytest

from logging import Logger
from unittest.mock import create_autospec

from src.backend.controllers.read_controller import MainController
from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.utils.db_schema_tables import create_tables

_main_controller = create_autospec(MainController)


@pytest.fixture
def logger():
    return create_autospec(Logger)


@pytest.fixture
def http_client():
    return create_autospec(HTTPClient)


@pytest.fixture
def database_client():
    return create_autospec(SQLClient)


@pytest.fixture
def plagiarism_client():
    return create_autospec(PlagiarismDetectorClient)


@pytest.fixture
def hdl_motor():
    return create_autospec(HDLMotor)



