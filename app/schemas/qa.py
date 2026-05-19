from typing import List, Optional

from pydantic import BaseModel, Field


class SourceChunk(BaseModel):
    source: str = Field(description="资料来源文件")
    chunk_id: int = Field(description="片段编号")
    score: float = Field(description="相似度分数")
    content: str = Field(description="参考片段内容")


class AskRequest(BaseModel):
    question: str = Field(..., min_length=2, description="用户问题")
    top_k: Optional[int] = Field(default=4, ge=1, le=8, description="召回片段数量")


class AskResponse(BaseModel):
    question: str
    answer: str
    sources: List[SourceChunk]
    elapsed_ms: int
    provider: str
    used_fallback: bool


class ToolRequest(BaseModel):
    text: str = Field(..., min_length=5, description="需要处理的文本")


class ToolResponse(BaseModel):
    result: str
