from dataclasses import dataclass
from typing import List

from app.services.document_loader import RawDocument


@dataclass
class TextChunk:
    source: str
    chunk_id: int
    content: str


class TextSplitter:
    """把长文档切成可检索片段。"""

    def __init__(self, chunk_size: int = 450, chunk_overlap: int = 80):
        if chunk_overlap >= chunk_size:
            raise ValueError("chunk_overlap 必须小于 chunk_size")
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def split_documents(self, documents: List[RawDocument]) -> List[TextChunk]:
        chunks: list[TextChunk] = []
        chunk_id = 1
        for doc in documents:
            for content in self._split_text(doc.content):
                chunks.append(TextChunk(source=doc.source, chunk_id=chunk_id, content=content))
                chunk_id += 1
        return chunks

    def _split_text(self, text: str) -> list[str]:
        clean_text = self._clean_text(text)
        if not clean_text:
            return []
        result: list[str] = []
        start = 0
        while start < len(clean_text):
            end = start + self.chunk_size
            part = clean_text[start:end].strip()
            if part:
                result.append(part)
            start = end - self.chunk_overlap
            if start < 0:
                start = 0
            if start >= len(clean_text):
                break
        return result

    def _clean_text(self, text: str) -> str:
        lines = [line.strip() for line in text.splitlines()]
        lines = [line for line in lines if line]
        return "\n".join(lines)
