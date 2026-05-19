from loguru import logger

from app.core.config import settings


def init_logger() -> None:
    """初始化日志。开发时输出到控制台，同时保存到文件。"""
    log_file = settings.log_path / "campus_qa_agent.log"
    logger.add(
        log_file,
        rotation="5 MB",
        retention="7 days",
        encoding="utf-8",
        enqueue=True,
    )
