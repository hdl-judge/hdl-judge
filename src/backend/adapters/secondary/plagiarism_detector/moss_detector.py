import mosspy

from typing import Text

from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient


class MossClient(PlagiarismDetectorClient):
    def __init__(self, userid: int, *args, **kwargs):
        self.userid = userid
        self.session = mosspy.Moss(userid, "vhdl")

    def get(self, url: Text, **kwargs):
        pass