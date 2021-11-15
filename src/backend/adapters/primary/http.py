from typing import Any
from logging import Logger

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime

from src.backend.controllers.read_controller import MainController
from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.adapters.primary.api.schemas.submission import Submission
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn
from src.backend.schema.request import UserModel, ProjectModel, ProjectFilesModel, TestbenchFiles, SubmissionFiles

from src.backend.dependencies import get_container
from dependency_injector.wiring import inject, Provide


class Response(BaseModel):
    query: str
    limit: int
    gifs: Any


router = APIRouter()
Container = get_container()


# @router.get('/', response_model=Response)
# @inject
# async def index(
#     http_adapter: HTTPClient = Depends(Provide[Container.http_client]),
# ):
#     controller = ReadController(logger=Logger, http_adapter=http_adapter)
#
#     request = controller.get_data()
#
#     return {
#         'query': "a",
#         'limit': 3,
#         'gifs': request.text,
#     }


@router.get('/plagiarism')
@inject
async def index(
    plagiarism_client: PlagiarismDetectorClient = Depends(Provide[Container.plagiarism_client]),
):
    controller = MainController(logger=Logger, plagiarism_client=plagiarism_client)
    response = controller.submit_codes_to_plagiarism()
    return response

  
@router.get('/config')
@inject
async def index(
    config: str = Depends(Provide[Container.config])
):
    return config


@router.post(
    "/submit",
    response_model=SubmissionReturn)
@inject
async def submit(
    submission: Submission,
    hdl_motor: HDLMotor = Depends(Provide[Container.hdl_motor])
):
    response = hdl_motor.get_waveform(submission.toplevel_entity, submission.files)
    return response


@router.get('/setup')
@inject
async def index(
   database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    request = controller.setup()
    return request


#Principal routes

@router.get('/get_values/{table_name}')
@inject
async def get_values(
    table_name: Text,
    id: Optional[Text] = None,
    database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.get_table_all_or_by_id(table_name, id)
    return response


@router.post('/create_user')
@inject
async def create_user(
    data: UserModel,
    database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_user(**data.dict())
    return response


@router.post('/create_project')
@inject
async def create_project(
    data: ProjectModel,
    database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_project(**data.dict())
    return response


@router.post('/create_projects_files')
@inject
async def create_projects_files(
    data: ProjectFilesModel,
    database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_projects_files(**data.dict())
    return response


@router.post('/create_testbench_files')
@inject
async def create_testbench_files(
    data: TestbenchFiles,
    database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_testbench_files(**data.dict())
    return response


@router.post('/create_submission_files')
@inject
async def create_submission_files(
    data: SubmissionFiles,
    database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_submission_files(**data.dict())
    return response



@router.get('/submit_all_codes_from_project_to_plagiarism')
@inject
async def submit_all_codes_from_project_to_plagiarism(
    project_id: int,
    plagiarism_client: PlagiarismDetectorClient = Depends(Provide[Container.plagiarism_client]),
):
    controller = MainController(logger=Logger, plagiarism_client=plagiarism_client)
    response = controller.submit_all_codes_from_project_to_plagiarism(
        project_id=project_id
    )
    return response

