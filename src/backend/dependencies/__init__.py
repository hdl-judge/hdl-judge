from dependency_injector import containers, providers

from src.backend.adapters.secondary.http.http_request import HTTPRequests


class Container(containers.DeclarativeContainer):

    config = providers.Configuration()

    http_client = providers.Factory(
        HTTPRequests
    )
