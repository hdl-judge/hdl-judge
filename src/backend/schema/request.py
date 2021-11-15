from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class UserModel(BaseModel):
    name: str
    email_address: str
    academic_id: str
    is_professor: Optional[bool] = False
    is_admin: Optional[bool] = False


class ProjectModel(BaseModel):
    name: str
    created_by: int
    due_time: datetime


class ProjectFilesModel(BaseModel):
    name: str
    created_by: int
    project_id: int


class TestbenchFiles(BaseModel):
    name: str
    created_by: int
    projects_files_id: int
    code: str


class SubmissionFiles(BaseModel):
    name: str
    created_by: int
    projects_files_id: int
    metadata: str
    code: str
