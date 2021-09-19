from typing import Any, Dict
from logging import Logger

from fastapi import APIRouter
from pydantic import BaseModel

from src.backend.controllers.read_controller import ReadController
from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor

from fastapi import Depends
from src.backend.dependencies import get_container
from dependency_injector.wiring import inject, Provide


class Response(BaseModel):
    query: str
    limit: int
    gifs: Any


class Submission(BaseModel):
    toplevel_entity: str
    files: Dict[str, str]


router = APIRouter()
Container = get_container()


@router.get('/', response_model=Response)
@inject
async def index(
    http_adapter: HTTPClient = Depends(Provide[Container.http_client]),
):
    controller = ReadController(Logger, http_adapter)

    request = controller.get_data()

    return {
        'query': "a",
        'limit': 3,
        'gifs': request.text,
    }


@router.get('/config')
@inject
async def index(
    config: str = Depends(Provide[Container.config])
):
    return config


@router.post('/submit')
@inject
async def submit(
    submission: Submission,
    hdl_motor: HDLMotor = Depends(Provide[Container.hdl_motor])
):
    return hdl_motor.get_waveform(submission.toplevel_entity, submission.files)
