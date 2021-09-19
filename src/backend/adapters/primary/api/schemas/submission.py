from typing import List
from pydantic import BaseModel


class File(BaseModel):
    filename: str
    content: str


class Submission(BaseModel):
    toplevel_entity: str
    files: List[File]
