from typing import Optional, List, Any
from logging import Logger

from fastapi import APIRouter
from pydantic import BaseModel

from src.backend.controllers.read_controller import ReadController
from src.backend.adapters.secondary.http import HTTPClient

from fastapi import Depends
from src.backend.dependencies import Container
from dependency_injector.wiring import inject, Provide

class Gif(BaseModel):
    url: str


class Response(BaseModel):
    query: str
    limit: int
    gifs: Any


router = APIRouter()


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