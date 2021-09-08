"""Application module."""

from fastapi import FastAPI

from src.backend.dependencies import Container
from src import server


def create_app() -> FastAPI:
    container = Container()
    container.config.from_yaml('config.yml')
    container.config.giphy.api_key.from_env('GIPHY_API_KEY')
    container.wire(modules=[server])

    app = FastAPI()
    app.container = container
    app.include_router(server.router)
    return app


app = create_app()