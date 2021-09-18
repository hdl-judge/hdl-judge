from abc import ABC, abstractmethod
from typing import Text, Dict


class HDLMotor(ABC):
    @abstractmethod
    def get_waveform(self, toplevel_entity: Text, files: Dict[Text, Text]) -> Text:
        pass
