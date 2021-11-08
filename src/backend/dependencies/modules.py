from dependency_injector import containers, providers
from unittest.mock import create_autospec

from src.backend.adapters.secondary.http.http_request import HTTPRequests
from src.backend.adapters.secondary.database.SQLAlchemy_client import SQLAlchemyClient
from src.backend.adapters.secondary.plagiarism_detector.moss_detector import MossClient
from src.backend.adapters.secondary.hdl_motor.ghdl_motor import GHDLMotor

from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor


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
    hdl_motor = providers.Factory(
        GHDLMotor
    )


class TestContainer(BaseContainer):
    http_client = providers.Factory(
        create_autospec(HTTPClient)
    )
    database_client = providers.Factory(
        create_autospec(SQLClient)
    )
    plagiarism_client = providers.Factory(
        create_autospec(PlagiarismDetectorClient),
        BaseContainer.config.BaseConfig.idMoss
    )
    hdl_motor = providers.Factory(
        create_autospec(HDLMotor)
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

