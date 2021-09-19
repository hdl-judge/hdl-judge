from dependency_injector import containers, providers

from src.backend.adapters.secondary.http.http_request import HTTPRequests
from src.backend.adapters.secondary.hdl_motor.ghdl_motor import GHDLMotor


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()


class ProductionContainer(BaseContainer):
    http_client = providers.Factory(
        HTTPRequests
    )


class TestContainer(BaseContainer):
    http_client = providers.Factory(
        HTTPRequests
    )


class DevelopmentContainer(BaseContainer):
    http_client = providers.Factory(HTTPRequests)
    hdl_motor = providers.Factory(GHDLMotor)
