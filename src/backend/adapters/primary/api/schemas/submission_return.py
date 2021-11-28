from typing import Optional

from pydantic import BaseModel

from src.backend.adapters.primary.api.schemas.response_status import ResponseStatus


class SubmissionReturn(BaseModel):
    status: ResponseStatus
    result: Optional[str]
    message: Optional[str]
    mimetype: Optional[str]
    filename: Optional[str]
