import pytest
import os

from typing import Any
from logging import Logger
from fastapi import APIRouter, Depends
from unittest import mock
from unittest.mock import create_autospec

from src.backend.controllers.read_controller import MainController
from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.adapters.primary.api.schemas.submission import Submission
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn

from src.backend.dependencies import get_container
from dependency_injector.wiring import inject, Provide

os.environ["SERVICE_ENV"] = "test"
Container = get_container()


@pytest.fixture(scope="session")
@inject
def controller(
    http_adapter: HTTPClient = Depends(Provide[Container.http_client]),
    plagiarism_client: PlagiarismDetectorClient = Depends(Provide[Container.plagiarism_client]),
    database_client: SQLClient = Depends(Provide[Container.database_client]),
    code_motor: HDLMotor = Depends(Provide[Container.hdl_motor])
):
    controller = MainController(
        logger=Logger,
        http_adapter=http_adapter,
        database_client=database_client,
        plagiarism_client=plagiarism_client,
        code_motor=code_motor
    )
    return controller


def test_base(controller):
    lalal = controller.get_data()
    assert lalal.code == 200