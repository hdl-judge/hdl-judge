import os

from dependency_injector import containers, providers

from src.backend.adapters.secondary.http.http_request import HTTPRequests
from src.backend.dependencies.modules import *


MODULE_MAP = {
    "production": ProductionContainer,
    "test": TestContainer,
    "development": DevelopmentContainer,
}


def get_container():
    env = os.getenv('SERVICE_ENV', 'development')
    return MODULE_MAP.get(env, DevelopmentContainer)
