from typing import Optional
from fastapi import File, Form, UploadFile
from pydantic import BaseModel


class FileMessage(BaseModel):
    question: str = Form(...)
    file: Optional[UploadFile] = File(None)
