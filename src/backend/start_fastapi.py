from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

from src.backend.dependencies import get_container
from src.backend.adapters.primary import http


def create_app(is_test: bool = False) -> FastAPI:

    if is_test:
        Container = get_container("test")
        container = Container()
        container.wire(modules=[http])
    else:
        Container = get_container()
        container = Container()
        container.wire(modules=[http])
        container.config.from_yaml('config.yml')

    app = FastAPI()

    origins = [
        "http://localhost:5000",
        "http://0.0.0.0:5000",
        "http://127.0.0.1:5000",
        "https://hdl-judge.brazilsouth.cloudapp.azure.com",
        "http://localhost:8000",
    ]

    app.container = container
    app.include_router(
        http.router,
        prefix="/api",
    )
    app.mount("/", StaticFiles(directory="static", html=True, check_dir=True), name="static")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app
  

app = create_app()
