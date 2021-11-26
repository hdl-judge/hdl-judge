from pydantic import BaseModel
from typing import Optional, List, Dict, Text, Any


class UserModel(BaseModel):
    name: str
    email_address: str
    academic_id: str
    is_professor: Optional[bool] = False
    is_admin: Optional[bool] = False


class ProjectModel(BaseModel):
    name: str
    created_by: int


class ProjectFilesModel(BaseModel):
    name: str
    project_id: int
    default_code: str


class TestbenchFiles(BaseModel):
    name: str
    created_by: int
    projects_files_id: int
    code: str


class SubmissionFiles(BaseModel):
    name: str
    project_id: int
    metadata: str
    code: str


class SaveSubmissionFilesDto(BaseModel):
    project_id: int
    files: List[Dict[Text, Any]]
