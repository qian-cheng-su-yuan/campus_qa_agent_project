from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.routes import router
from app.core.config import settings
from app.core.logger import init_logger

init_logger()

app = FastAPI(
    title=settings.app_name,
    description="校园智能问答助手：RAG 知识库问答 + Agent 工具能力",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
def root() -> dict:
    return {
        "message": "Campus QA Agent API is running.",
        "docs": "/docs",
        "health": "/api/v1/health",
    }
