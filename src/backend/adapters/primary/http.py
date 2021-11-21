from typing import Any
from logging import Logger

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import Optional, Text
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext

from src.backend.controllers.read_controller import MainController
from src.backend.adapters.secondary.database import SQLClient
from src.backend.adapters.secondary.plagiarism_detector import PlagiarismDetectorClient
from src.backend.adapters.secondary.hdl_motor import HDLMotor
from src.backend.adapters.primary.api.schemas.submission import Submission
from src.backend.adapters.primary.api.schemas.submission_return import SubmissionReturn
from src.backend.schema.request import UserModel, ProjectModel, ProjectFilesModel, TestbenchFiles, SubmissionFiles

from src.backend.dependencies import get_container
from dependency_injector.wiring import inject, Provide


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")


router = APIRouter()
Container = get_container()


class Response(BaseModel):
    query: str
    limit: int
    gifs: Any


class User(BaseModel):
    id: int
    name: Optional[str] = None
    email_address: Optional[str] = None
    academic_id: Optional[str] = None
    is_professor: bool
    is_admin: bool


def create_access_token(
        data: dict,
        expires_delta: Optional[timedelta] = None,
        config: str = Depends(Provide[Container.config])
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=config.ALGORITHM)
    return encoded_jwt


@inject
async def get_current_user(
        token: str = Depends(oauth2_scheme),
        database_client: SQLClient = Depends(Provide[Container.database_client]),
        config: str = Depends(Provide[Container.config])
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[config.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    controller = MainController(logger=Logger, database_client=database_client)
    user = controller.get_user_by_email(username)
    if user is None:
        raise credentials_exception
    return user


# @router.get('/', response_model=Response)
# @inject
# async def index(
#     http_adapter: HTTPClient = Depends(Provide[Container.http_client]),
# ):
#     controller = ReadController(logger=Logger, http_adapter=http_adapter)
#
#     request = controller.get_data()
#
#     return {
#         'query': "a",
#         'limit': 3,
#         'gifs': request.text,
#     }


@router.get('/plagiarism')
@inject
async def index(
        plagiarism_client: PlagiarismDetectorClient = Depends(Provide[Container.plagiarism_client]),
):
    controller = MainController(logger=Logger, plagiarism_client=plagiarism_client)
    response = controller.submit_codes_to_plagiarism()
    return response


@router.get('/config')
@inject
async def index(
        config: str = Depends(Provide[Container.config])
):
    return config


@router.post(
    "/submit",
    response_model=SubmissionReturn)
@inject
async def submit(
        submission: Submission,
        hdl_motor: HDLMotor = Depends(Provide[Container.hdl_motor])
):
    response = hdl_motor.get_waveform(submission.toplevel_entity, submission.files)
    return response


@router.get('/setup')
@inject
async def setup(
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    request = controller.setup()
    return request


@router.get("/users/me")
async def read_users_me(
        current_user: User = Depends(get_current_user)
):
    return current_user


@router.post("/token")
@inject
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        database_client: SQLClient = Depends(Provide[Container.database_client]),
        config: str = Depends(Provide[Container.config])
):
    controller = MainController(logger=Logger, database_client=database_client)
    user = controller.get_user_by_email(form_data.username)
    if not user or not pwd_context.verify(form_data.password, user["hashed_password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email_address"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# Main routes


@router.get('/get_values/{table_name}')
@inject
async def get_values(
        table_name: Text,
        id: Optional[Text] = None,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.get_table_all_or_by_id(table_name, id)
    return response


@router.delete('/delete_value/{table_name}')
@inject
async def delete_value(
        table_name: Text,
        id: int,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.delete_record_by_id(table_name, id)
    return response


@router.post('/create_user')
@inject
async def create_user(
        data: UserModel,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_user(**data.dict())
    return response


@router.post('/create_project')
@inject
async def create_project(
        data: ProjectModel,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_project(**data.dict())
    return response


@router.post('/create_projects_files')
@inject
async def create_projects_files(
        data: ProjectFilesModel,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_projects_files(**data.dict())
    return response


@router.post('/create_testbench_files')
@inject
async def create_testbench_files(
        data: TestbenchFiles,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_testbench_files(**data.dict())
    return response


@router.post('/create_submission_files')
@inject
async def create_submission_files(
        data: SubmissionFiles,
        database_client: SQLClient = Depends(Provide[Container.database_client]),
):
    controller = MainController(logger=Logger, database_client=database_client)
    response = controller.create_submission_files(**data.dict())
    return response


@router.get('/submit_all_codes_from_project_to_plagiarism')
@inject
async def submit_all_codes_from_project_to_plagiarism(
        project_id: int,
        plagiarism_client: PlagiarismDetectorClient = Depends(Provide[Container.plagiarism_client]),
):
    controller = MainController(logger=Logger, plagiarism_client=plagiarism_client)
    response = controller.submit_all_codes_from_project_to_plagiarism(
        project_id=project_id
    )
    return response
