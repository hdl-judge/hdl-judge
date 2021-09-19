from logging import Logger
from typing import Optional, List, Any, Dict, Text

from src.backend.controllers import BaseController

from src.backend.adapters.secondary.http import HTTPClient
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient


class ReadController(BaseController):
    @property
    def POSTS_ENDPOINT(self):
        return "https://www.uol.com.br/"

    def __init__(
        self,
        logger: Logger = None,
        http_adapter: HTTPClient = None,
        database_client: SQLClient = None,
        plagiarism_client: PlagiarismDetectorClient = None
    ):
        super().__init__(logger)
        self.http_adapter = http_adapter
        self.database_client = database_client
        self.plagiarism_client = plagiarism_client

    def get_data(self) -> Dict[Text, Any]:
        result = self.http_adapter.get(self.POSTS_ENDPOINT)
        return result

    def submit_codes_to_plagiarism(self):
        file = open("C:\\Users\\felip\\Documents\\GitHub\\hdl-judge\\test_moss\\subs\\F_POLI-1.vhd", 'r')
        code = file.read()
        file.close()

        #self.plagiarism_client.add_base_file({"test1.vhd": code})
        self.plagiarism_client.add_student_files(1, {"test1.vhd": code})
        self.plagiarism_client.add_student_files(2, {"test2.vhd": code})
        self.plagiarism_client.add_student_files(3, {"test3.vhd": code})
        url, report_as_text = self.plagiarism_client.generate_report()
        self.plagiarism_client.clean()
        return url

    def get_config(self) -> Any:
        return True
