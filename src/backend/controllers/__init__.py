from abc import ABC

from logging import Logger


class BaseController(ABC):
    def __init__(self, logger: Logger):
        self.logger = logger
