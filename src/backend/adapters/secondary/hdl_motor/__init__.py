from abc import ABC, abstractmethod
from typing import Text, List

from src.backend.adapters.primary.api.schemas.submission import File
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn


class HDLMotor(ABC):
    @abstractmethod
    def get_waveform(self, files: List[File]) -> SubmissionReturn:
        pass
