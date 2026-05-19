from dataclasses import dataclass
from pathlib import Path
from typing import List

from pypdf import PdfReader

from app.utils.file_utils import list_supported_files


@dataclass
class RawDocument:
    source: str
    content: str


class DocumentLoader:
    """负责读取知识库文档。当前支持 TXT / MD / PDF。"""

    def load_from_directory(self, directory: Path) -> List[RawDocument]:
        documents: list[RawDocument] = []
        for file_path in list_supported_files(directory):
            content = self.load_file(file_path)
            if content.strip():
                documents.append(RawDocument(source=file_path.name, content=content))
        return documents

    def load_file(self, file_path: Path) -> str:
        suffix = file_path.suffix.lower()
        if suffix in {".txt", ".md"}:
            return file_path.read_text(encoding="utf-8", errors="ignore")
        if suffix == ".pdf":
            return self._load_pdf(file_path)
        raise ValueError(f"不支持的文件格式：{suffix}")

    def _load_pdf(self, file_path: Path) -> str:
        reader = PdfReader(str(file_path))
        pages: list[str] = []
        for page in reader.pages:
            pages.append(page.extract_text() or "")
        return "\n".join(pages)
