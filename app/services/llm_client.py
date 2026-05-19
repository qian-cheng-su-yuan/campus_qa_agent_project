from __future__ import annotations

import requests
from loguru import logger

from app.core.config import settings


class LLMClient:
    """OpenAI-Compatible 大模型调用封装。"""

    def __init__(self):
        self.provider = settings.llm_provider
        self.base_url = settings.llm_base_url.rstrip("/")
        self.model = settings.llm_model
        self.api_key = settings.llm_api_key
        self.timeout = settings.llm_timeout

    @property
    def available(self) -> bool:
        return bool(self.api_key and self.base_url and self.model)

    def chat(self, system_prompt: str, user_prompt: str) -> tuple[str, bool]:
        """返回：answer, used_fallback。"""
        if not self.available:
            if settings.enable_local_fallback:
                return self._fallback_answer(user_prompt), True
            raise RuntimeError("未配置 LLM_API_KEY，且未启用本地兜底模式")

        url = f"{self.base_url}/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            return content.strip(), False
        except Exception as exc:  # noqa: BLE001
            logger.exception("调用大模型失败：{}", exc)
            if settings.enable_local_fallback:
                return self._fallback_answer(user_prompt), True
            raise

    def _fallback_answer(self, user_prompt: str) -> str:
        # 从 Prompt 中截取参考资料，生成一个可演示的本地回答。
        marker = "【参考资料】"
        question_marker = "【用户问题】"
        context = user_prompt
        question = ""
        if marker in user_prompt:
            context = user_prompt.split(marker, 1)[1]
        if question_marker in context:
            context_part, question_part = context.split(question_marker, 1)
            context = context_part.strip()
            question = question_part.strip()
        if "【回答要求】" in question:
            question = question.split("【回答要求】", 1)[0].strip()

        lines = [line.strip() for line in context.splitlines() if line.strip()]
        useful_lines = [line for line in lines if not line.startswith("片段")][:8]
        if not useful_lines:
            return "知识库中没有检索到足够明确的依据，暂时无法给出确定回答。建议补充相关校园制度或通知后再查询。"

        answer_lines = [
            "根据当前知识库资料，可以这样处理：",
            "",
        ]
        for idx, line in enumerate(useful_lines[:5], start=1):
            answer_lines.append(f"{idx}. {line[:160]}")
        answer_lines.extend(
            [
                "",
                "注意：当前回答由本地兜底模式生成，适合演示 RAG 流程。配置 API Key 后会调用真实大模型生成更自然的回答。",
            ]
        )
        if question:
            answer_lines.insert(0, f"问题：{question}")
        return "\n".join(answer_lines)
