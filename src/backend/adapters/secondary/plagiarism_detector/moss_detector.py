import mosspy
import tempfile
import logging
import os

from typing import Text, Dict

from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient


class MossClient(PlagiarismDetectorClient):
    BASE_STUDENT_PATH = "student_files"
    BASE_BASE_PATH = "base_files"
    BASE_REPORT_PATH = "report"

    def __init__(self, userid: int, *args, **kwargs):
        self.userid = userid
        self.mosspy = mosspy.Moss(userid, "vhdl")
        self._f = tempfile.TemporaryDirectory()

        logging.debug(f"Temp directory created in {self._f.name}")

    def add_base_file(self, base_codes: Dict[Text, Text]):
        for filename, code in base_codes.items():
            path = self.join_path(self._f.name, self.join_path(self.BASE_BASE_PATH, filename))
            directory = self.join_path(self._f.name, self.BASE_BASE_PATH)
            if not os.path.exists(directory):
                logging.debug(f"Creating directory in {directory}")
                os.makedirs(directory)
            display_name = f"BASE-{filename}"

            file = open(path, 'w')
            file.write(code)
            file.close()

            self.mosspy.addBaseFile(path, display_name)

    def add_student_files(self, student_id, base_codes: Dict[Text, Text]):
        for filename, code in base_codes.items():
            student_sub_path = self.join_path(self.BASE_STUDENT_PATH, str(student_id))
            directory = self.join_path(self._f.name, student_sub_path)
            if not os.path.exists(directory):
                logging.debug(f"Creating directory in {directory}")
                os.makedirs(directory)

            path = self.join_path(self._f.name, self.join_path(student_sub_path, filename))
            display_name = f"{student_id}-{filename}"

            logging.debug(f"Adding file {path} as {display_name}")
            file = open(path, 'w')
            file.write(code)
            file.close()

            self.mosspy.addFile(path, display_name)

    def generate_report(self) -> (Text, Text):
        report_path = self.join_path(self._f.name, self.join_path(self.BASE_REPORT_PATH, "report.html"))
        directory = self.join_path(self._f.name, self.BASE_REPORT_PATH)
        if not os.path.exists(directory):
            logging.debug(f"Creating directory in {directory}")
            os.makedirs(directory)

        logging.debug("Sending Data")
        url = self.mosspy.send(lambda file_path, display_name: logging.debug(f"Sending {file_path} as {display_name}"))
        logging.info(f"Data processed. URL: {url}")

        logging.debug(f"Downloading report to {report_path}")
        self.mosspy.saveWebPage(url, report_path)
        logging.debug(f"Opening report from {report_path}")
        with open(report_path, 'r') as file:
            report_as_text = file.read()

        return url, report_as_text

    def clean(self):
        logging.debug(f"Cleaning everything from {self._f.name}")
        self._f.cleanup()
        del self.mosspy

    @staticmethod
    def join_path(base_path, additional_path):
        return os.path.join(base_path, additional_path)
