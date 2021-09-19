from dependency_injector import containers, providers

from src.backend.adapters.secondary.http.http_request import HTTPRequests
from src.backend.adapters.secondary.database.SQLAlchemy_client import SQLAlchemyClient
from src.backend.adapters.secondary.plagiarism_detector.moss_detector import MossClient
from src.backend.adapters.secondary.hdl_motor.ghdl_motor import GHDLMotor


class BaseContainer(containers.DeclarativeContainer):
    config = providers.Configuration()
    print(config)


class ProductionContainer(BaseContainer):
    http_client = providers.Factory(
        HTTPRequests
    )
    database_client = providers.Factory(
        SQLAlchemyClient
    )
    plagiarism_client = providers.Factory(
        MossClient,
        BaseContainer.config.BaseConfig.idMoss
    )


class TestContainer(BaseContainer):
    http_client = providers.Factory(
        HTTPRequests
    )
    database_client = providers.Factory(
        SQLAlchemyClient
    )
    plagiarism_client = providers.Factory(
        MossClient,
        BaseContainer.config.BaseConfig.idMoss
    )


class DevelopmentContainer(BaseContainer):
    http_client = providers.Factory(
        HTTPRequests
    )
    database_client = providers.Factory(
        SQLAlchemyClient
    )
    plagiarism_client = providers.Factory(
        MossClient,
        BaseContainer.config.BaseConfig.idMoss
    )
    hdl_motor = providers.Factory(
      GHDLMotor
    )

