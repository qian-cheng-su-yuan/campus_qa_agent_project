# 校园智能问答助手 Campus QA Agent

> 一个面向校园服务场景的 RAG 知识库问答项目，适合放入简历、面试展示和本地演示。项目采用“FastAPI 后端 + Streamlit 演示前端 + 服务层拆分 + OpenAI-Compatible 大模型接口”的企业常见写法。

## 1. 项目定位

本项目面向高校学生常见办事咨询场景，例如宿舍报修、考试安排、请假流程、就业材料、图书馆服务等。系统将校园制度、办事流程、FAQ 文档整理成知识库，通过检索增强生成（RAG）实现“基于资料回答问题”的智能问答能力。

项目不是简单调用大模型聊天，而是把企业项目里常见的几个模块拆开：

- 文档解析：读取校园制度、FAQ、通知类文本；
- 文本切分：将长文档切成可检索片段；
- 检索召回：根据用户问题找到相关资料；
- Prompt 组装：把问题和参考资料拼接给大模型；
- 大模型调用：支持接入 Qwen / DeepSeek / OpenAI-Compatible API；
- Agent 工具：提供文档总结、关键词提取、办事清单生成；
- Web 演示：使用 Streamlit 提供可视化页面；
- API 服务：使用 FastAPI 提供标准接口，便于后续接入前端或小程序。

## 2. 项目亮点

### 2.1 更接近企业项目结构

```text
campus_qa_agent_project/
├── app/
│   ├── api/                 # 路由层
│   ├── core/                # 配置、日志
│   ├── schemas/             # 请求/响应模型
│   ├── services/            # 业务服务层
│   ├── utils/               # 工具函数
│   └── main.py              # FastAPI 入口
├── data/
│   ├── knowledge_base/      # 示例校园知识库
│   └── uploads/             # 上传文件目录
├── docs/                    # 项目说明文档
├── tests/                   # 简单测试
├── web/                     # Streamlit 前端
├── .env.example             # 环境变量模板
├── requirements.txt         # 依赖
├── run_api.py               # 启动后端
└── run_web.py               # 启动前端
```

### 2.2 支持 API Key 接入

本项目支持 OpenAI-Compatible 接口。你可以接入：

- 阿里云百炼 Qwen
- DeepSeek
- OpenAI-Compatible 私有网关
- 其他兼容 `/chat/completions` 的大模型平台

没有配置 API Key 时，系统会启用本地兜底回答，方便在面试现场无网络或 Key 不可用时演示完整流程。

### 2.3 适合面试展示

面试时可以重点讲这条链路：

```text
用户问题 → 文档切分 → 知识库检索 → 上下文拼接 → Prompt 约束 → 大模型生成 → 参考片段展示
```

这个链路比“只做一个聊天页面”更有技术含量，也更符合 AI 应用开发岗位、RAG 应用开发岗位和 AI 应用后端岗位的项目要求。

## 3. 运行环境

建议使用：

- Python 3.10 或 3.11
- PyCharm
- Windows / macOS / Linux 均可

## 4. PyCharm 运行步骤

### 第一步：打开项目

1. 解压本项目压缩包；
2. 打开 PyCharm；
3. 点击 `File` → `Open`；
4. 选择 `campus_qa_agent_project` 文件夹。

### 第二步：创建虚拟环境

在 PyCharm 终端执行：

```bash
python -m venv .venv
```

Windows 激活：

```bash
.venv\Scripts\activate
```

macOS / Linux 激活：

```bash
source .venv/bin/activate
```

### 第三步：安装依赖

国内网络建议使用清华镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 第四步：配置 API Key

复制环境变量模板：

```bash
copy .env.example .env
```

macOS / Linux：

```bash
cp .env.example .env
```

然后打开 `.env`，填写你的 API Key。例如阿里云百炼：

```env
LLM_PROVIDER=qwen
LLM_API_KEY=你的API_KEY
LLM_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
LLM_MODEL=qwen-plus
```

如果你暂时不配置 API Key，也可以直接运行，系统会用本地兜底模式演示。

### 第五步：启动后端 API

```bash
python run_api.py
```

浏览器打开：

```text
http://127.0.0.1:8000/docs
```

可以看到 FastAPI 自动生成的接口文档。

### 第六步：启动前端页面

另开一个终端，执行：

```bash
python run_web.py
```

浏览器打开：

```text
http://127.0.0.1:8501
```

## 5. API 示例

### 健康检查

```bash
curl http://127.0.0.1:8000/api/v1/health
```

### 问答接口

```bash
curl -X POST http://127.0.0.1:8000/api/v1/ask ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"学生请假需要哪些材料？\",\"top_k\":3}"
```

macOS / Linux：

```bash
curl -X POST http://127.0.0.1:8000/api/v1/ask \
  -H "Content-Type: application/json" \
  -d '{"question":"学生请假需要哪些材料？","top_k":3}'
```

## 6. 可演示问题

你可以在页面中测试这些问题：

- 学生请假需要哪些材料？
- 宿舍水电故障应该怎么报修？
- 图书馆借书可以借多久？
- 就业推荐表丢了怎么办？
- 期末考试缓考怎么申请？
- 校园卡丢失后怎么补办？
