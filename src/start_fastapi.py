from fastapi import FastAPI

from src.backend.dependencies import get_container
from src.backend.adapters.primary import http


def create_app() -> FastAPI:

    Container = get_container()
    container = Container()
    container.config.from_yaml('config.yml')
    container.wire(modules=[http])

    app = FastAPI()
    app.container = container
    app.include_router(http.router)
    return app


app = create_app()