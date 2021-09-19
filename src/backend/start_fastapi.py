from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.backend.dependencies import get_container
from src.backend.adapters.primary import http


def create_app() -> FastAPI:

    Container = get_container()
    container = Container()
    container.config.from_yaml('config.yml')
    container.wire(modules=[http])

    app = FastAPI()

    origins = [
        "http://localhost:5000"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.container = container
    app.include_router(http.router)
    return app


app = create_app()
