from typing import Any
from logging import Logger

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from src.backend.controllers.read_controller import ReadController
from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.adapters.primary.api.schemas.submission import Submission
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn


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
    controller = ReadController(logger=Logger, plagiarism_client=plagiarism_client)
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
    controller = ReadController(logger=Logger, database_client=database_client)
    request = controller.setup()
    return request