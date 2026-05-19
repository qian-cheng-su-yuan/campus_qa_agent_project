from typing import List

from pydantic import BaseModel


class DocumentInfo(BaseModel):
    file_name: str
    size: int
    suffix: str


class RebuildResponse(BaseModel):
    document_count: int
    chunk_count: int
    message: str


class UploadResponse(BaseModel):
    saved_files: List[DocumentInfo]
    message: str
