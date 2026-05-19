from fastapi import APIRouter, File, HTTPException, UploadFile

from app.core.config import settings
from app.schemas.document import DocumentInfo, RebuildResponse, UploadResponse
from app.schemas.qa import AskRequest, AskResponse, ToolRequest, ToolResponse
from app.services.rag_service import rag_service
from app.utils.file_utils import ALLOWED_SUFFIXES, safe_filename

router = APIRouter(prefix="/api/v1", tags=["campus-qa-agent"])


@router.get("/health")
def health() -> dict:
    return {
        "status": "ok",
        "app_name": settings.app_name,
        "provider": settings.llm_provider,
        "chunk_count": rag_service.chunk_count,
    }


@router.post("/ask", response_model=AskResponse)
def ask(request: AskRequest) -> AskResponse:
    return rag_service.ask(question=request.question, top_k=request.top_k)


@router.post("/knowledge/rebuild", response_model=RebuildResponse)
def rebuild_knowledge_base() -> RebuildResponse:
    document_count, chunk_count = rag_service.rebuild_index()
    return RebuildResponse(
        document_count=document_count,
        chunk_count=chunk_count,
        message="知识库重建完成",
    )


@router.post("/knowledge/upload", response_model=UploadResponse)
async def upload_files(files: list[UploadFile] = File(...)) -> UploadResponse:
    saved: list[DocumentInfo] = []
    for file in files:
        name = safe_filename(file.filename or "uploaded.txt")
        suffix = "." + name.rsplit(".", 1)[-1].lower() if "." in name else ""
        if suffix not in ALLOWED_SUFFIXES:
            raise HTTPException(status_code=400, detail=f"不支持的文件格式：{suffix}")
        content = await file.read()
        rag_service.save_uploaded_file(name, content)
        saved.append(DocumentInfo(file_name=name, size=len(content), suffix=suffix))

    rag_service.rebuild_index()
    return UploadResponse(saved_files=saved, message="文件上传并重建知识库完成")


@router.post("/tools/summarize", response_model=ToolResponse)
def summarize(request: ToolRequest) -> ToolResponse:
    return ToolResponse(result=rag_service.summarize_text(request.text))


@router.post("/tools/keywords", response_model=ToolResponse)
def keywords(request: ToolRequest) -> ToolResponse:
    return ToolResponse(result=rag_service.extract_keywords(request.text))


@router.post("/tools/todo", response_model=ToolResponse)
def todo(request: ToolRequest) -> ToolResponse:
    return ToolResponse(result=rag_service.make_todo_list(request.text))
