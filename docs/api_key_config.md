# API Key 配置说明

本项目使用 OpenAI-Compatible 方式调用大模型，也就是接口格式接近 OpenAI 的 `/chat/completions`。

## 1. 阿里云百炼 Qwen 示例

在 `.env` 中填写：

```env
LLM_PROVIDER=qwen
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
LLM_API_KEY=你的阿里云百炼APIKey
```

然后重启后端：

```bash
python run_api.py
```

## 2. DeepSeek 示例

```env
LLM_PROVIDER=deepseek
LLM_BASE_URL=https://api.deepseek.com
LLM_MODEL=deepseek-chat
LLM_API_KEY=你的DeepSeekAPIKey
```

## 3. 其他 OpenAI-Compatible 网关

```env
LLM_PROVIDER=openai_compatible
LLM_BASE_URL=https://你的网关地址/v1
LLM_MODEL=你的模型名称
LLM_API_KEY=你的APIKey
```

## 4. 没有 API Key 怎么办

如果 `.env` 中没有配置 `LLM_API_KEY`，并且：

```env
ENABLE_LOCAL_FALLBACK=true
```

系统会自动启用本地兜底回答。这个模式不会调用大模型，但可以展示完整的 RAG 检索流程。
