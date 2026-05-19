import re
from collections import Counter


class AgentTools:
    """简单 Agent 工具能力。

    这些工具不是复杂 Agent 框架，而是面试项目中容易解释的工具函数：
    - 文档总结
    - 关键词提取
    - 办事清单生成
    """

    def summarize(self, text: str, max_sentences: int = 5) -> str:
        sentences = re.split(r"[。！？!?\n]", text)
        sentences = [item.strip() for item in sentences if item.strip()]
        if not sentences:
            return "没有可总结的内容。"
        selected = sentences[:max_sentences]
        return "\n".join(f"- {item}" for item in selected)

    def extract_keywords(self, text: str, top_k: int = 8) -> str:
        tokens = re.findall(r"[\u4e00-\u9fff]{2,4}|[a-zA-Z][a-zA-Z0-9_]+", text)
        stopwords = {"学生", "需要", "进行", "可以", "相关", "如果", "申请", "办理", "按照", "材料"}
        counter = Counter(token for token in tokens if token not in stopwords)
        if not counter:
            return "未提取到明显关键词。"
        return "、".join(token for token, _ in counter.most_common(top_k))

    def make_todo_list(self, text: str) -> str:
        lines = [line.strip(" -\t") for line in text.splitlines() if line.strip()]
        candidates = [line for line in lines if any(key in line for key in ["提交", "填写", "联系", "上传", "确认", "办理", "携带", "申请"])]
        if not candidates:
            return "当前文本中没有识别到明显的待办事项。"
        return "\n".join(f"☐ {line}" for line in candidates[:10])
