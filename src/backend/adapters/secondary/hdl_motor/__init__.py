from abc import ABC, abstractmethod
from typing import Text, List

from src.backend.adapters.primary.api.schemas.submission import File


class HDLMotor(ABC):
    @abstractmethod
    def get_waveform(self, toplevel_entity: Text, files: List[File]) -> Text:
        pass
