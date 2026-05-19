from __future__ import annotations

import time
from pathlib import Path
from typing import List

from loguru import logger

from app.core.config import settings
from app.schemas.qa import AskResponse, SourceChunk
from app.services.agent_tools import AgentTools
from app.services.document_loader import DocumentLoader
from app.services.llm_client import LLMClient
from app.services.retriever import RetrievedChunk, SimpleRetriever
from app.services.text_splitter import TextSplitter


class RAGService:
    """RAG 主流程编排层。"""

    def __init__(self):
        self.loader = DocumentLoader()
        self.splitter = TextSplitter(settings.chunk_size, settings.chunk_overlap)
        self.retriever = SimpleRetriever()
        self.llm = LLMClient()
        self.tools = AgentTools()
        self._chunk_count = 0
        self.rebuild_index()

    @property
    def chunk_count(self) -> int:
        return self._chunk_count

    def rebuild_index(self) -> tuple[int, int]:
        documents = self.loader.load_from_directory(settings.knowledge_path)
        upload_docs = self.loader.load_from_directory(settings.upload_path)
        all_documents = documents + upload_docs
        chunks = self.splitter.split_documents(all_documents)
        self.retriever.build(chunks)
        self._chunk_count = len(chunks)
        logger.info("知识库重建完成，文档数：{}，片段数：{}", len(all_documents), len(chunks))
        return len(all_documents), len(chunks)

    def ask(self, question: str, top_k: int | None = None) -> AskResponse:
        start = time.perf_counter()
        top_k = top_k or settings.default_top_k
        retrieved = self.retriever.search(question, top_k=top_k)
        system_prompt = self._build_system_prompt()
        user_prompt = self._build_user_prompt(question, retrieved)
        answer, used_fallback = self.llm.chat(system_prompt, user_prompt)
        elapsed_ms = int((time.perf_counter() - start) * 1000)

        logger.info(
            "question={} top_k={} hit_count={} elapsed_ms={} fallback={}",
            question,
            top_k,
            len(retrieved),
            elapsed_ms,
            used_fallback,
        )

        return AskResponse(
            question=question,
            answer=answer,
            sources=[
                SourceChunk(
                    source=item.source,
                    chunk_id=item.chunk_id,
                    score=item.score,
                    content=item.content,
                )
                for item in retrieved
            ],
            elapsed_ms=elapsed_ms,
            provider=settings.llm_provider,
            used_fallback=used_fallback,
        )

    def save_uploaded_file(self, file_name: str, content: bytes) -> Path:
        target = settings.upload_path / file_name
        target.write_bytes(content)
        return target

    def summarize_text(self, text: str) -> str:
        return self.tools.summarize(text)

    def extract_keywords(self, text: str) -> str:
        return self.tools.extract_keywords(text)

    def make_todo_list(self, text: str) -> str:
        return self.tools.make_todo_list(text)

    def _build_system_prompt(self) -> str:
        return (
            "你是一个校园智能问答助手，主要帮助学生查询校园办事流程、制度说明和常见问题。"
            "回答必须优先依据给定参考资料，不要编造学校不存在的规定。"
            "如果资料中没有明确依据，要说明‘知识库中未找到明确说明’。"
            "办事类问题请尽量按步骤回答，并列出所需材料、办理地点、注意事项。"
            "语言要清楚、简洁，适合普通学生阅读。"
        )

    def _build_user_prompt(self, question: str, chunks: List[RetrievedChunk]) -> str:
        if not chunks:
            context = "知识库未检索到相关片段。"
        else:
            context_parts = []
            for idx, chunk in enumerate(chunks, start=1):
                context_parts.append(
                    f"片段{idx}｜来源：{chunk.source}｜相似度：{chunk.score}\n{chunk.content}"
                )
            context = "\n\n".join(context_parts)

        return f"""
【参考资料】
{context}

【用户问题】
{question}

【回答要求】
1. 先给出直接结论；
2. 如果是流程类问题，用 1、2、3 分步骤说明；
3. 必要时列出材料、地点、时间限制和注意事项；
4. 不要编造参考资料中没有的信息；
5. 最后提醒学生以学院或学校最新通知为准。
""".strip()


rag_service = RAGService()
