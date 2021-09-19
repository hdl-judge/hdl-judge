from abc import ABC, abstractmethod
from typing import Any, Text, Dict


class PlagiarismDetectorClient(ABC):
    def __init__(self, *args, **kwargs):
        pass

    @abstractmethod
    def add_base_file(self, base_codes: Dict[Text, Text]):
        pass

    @abstractmethod
    def add_student_files(self, student_id, base_codes: Dict[Text, Text]):
        pass

    @abstractmethod
    def generate_report(self) -> (Text, Text):
        pass

    @abstractmethod
    def clean(self):
        pass
