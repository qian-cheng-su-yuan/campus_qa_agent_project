import math
import re
from collections import Counter
from dataclasses import dataclass
from typing import List

from app.services.text_splitter import TextChunk


@dataclass
class RetrievedChunk:
    source: str
    chunk_id: int
    content: str
    score: float


class SimpleRetriever:
    """轻量本地检索器。

    面试演示项目不强制依赖向量数据库，先用 TF-IDF 思路实现本地检索。
    后续可以替换为 Chroma / FAISS / Milvus。
    """

    def __init__(self):
        self.chunks: list[TextChunk] = []
        self.doc_tokens: list[Counter[str]] = []
        self.idf: dict[str, float] = {}

    def build(self, chunks: List[TextChunk]) -> None:
        self.chunks = chunks
        self.doc_tokens = [Counter(self._tokenize(chunk.content)) for chunk in chunks]
        self._build_idf()

    def search(self, query: str, top_k: int = 4) -> list[RetrievedChunk]:
        if not self.chunks:
            return []

        query_vec = self._to_tfidf(Counter(self._tokenize(query)))
        scored: list[RetrievedChunk] = []
        for chunk, token_counter in zip(self.chunks, self.doc_tokens):
            doc_vec = self._to_tfidf(token_counter)
            score = self._cosine(query_vec, doc_vec)
            if score > 0:
                scored.append(
                    RetrievedChunk(
                        source=chunk.source,
                        chunk_id=chunk.chunk_id,
                        content=chunk.content,
                        score=round(score, 4),
                    )
                )

        scored.sort(key=lambda item: item.score, reverse=True)
        return scored[:top_k]

    def _build_idf(self) -> None:
        total_docs = len(self.doc_tokens)
        df: Counter[str] = Counter()
        for counter in self.doc_tokens:
            for token in counter.keys():
                df[token] += 1
        self.idf = {
            token: math.log((1 + total_docs) / (1 + freq)) + 1
            for token, freq in df.items()
        }

    def _to_tfidf(self, counter: Counter[str]) -> dict[str, float]:
        if not counter:
            return {}
        total = sum(counter.values())
        return {
            token: (count / total) * self.idf.get(token, 1.0)
            for token, count in counter.items()
        }

    def _cosine(self, left: dict[str, float], right: dict[str, float]) -> float:
        if not left or not right:
            return 0.0
        common = set(left.keys()) & set(right.keys())
        numerator = sum(left[token] * right[token] for token in common)
        left_norm = math.sqrt(sum(value * value for value in left.values()))
        right_norm = math.sqrt(sum(value * value for value in right.values()))
        if left_norm == 0 or right_norm == 0:
            return 0.0
        return numerator / (left_norm * right_norm)

    def _tokenize(self, text: str) -> list[str]:
        text = text.lower()
        chinese = re.findall(r"[\u4e00-\u9fff]{1,4}", text)
        english = re.findall(r"[a-zA-Z0-9_]+", text)

        # 中文采用 1-2 字符滑窗，保证“请假/宿舍/图书馆”等短词能被召回。
        zh_tokens: list[str] = []
        for word in chinese:
            if len(word) <= 2:
                zh_tokens.append(word)
            else:
                zh_tokens.extend(word[i : i + 2] for i in range(len(word) - 1))
        return zh_tokens + english
