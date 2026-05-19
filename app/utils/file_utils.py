from pathlib import Path
from typing import Iterable

ALLOWED_SUFFIXES = {".txt", ".md", ".pdf"}


def list_supported_files(directory: Path) -> list[Path]:
    directory.mkdir(parents=True, exist_ok=True)
    files: list[Path] = []
    for item in directory.rglob("*"):
        if item.is_file() and item.suffix.lower() in ALLOWED_SUFFIXES:
            files.append(item)
    return sorted(files)


def safe_filename(name: str) -> str:
    """简单文件名清理，避免上传文件名包含路径。"""
    name = Path(name).name.strip()
    for ch in ['/', '\\', ':', '*', '?', '"', '<', '>', '|']:
        name = name.replace(ch, '_')
    return name or "uploaded.txt"


def ensure_directories(paths: Iterable[Path]) -> None:
    for path in paths:
        path.mkdir(parents=True, exist_ok=True)
