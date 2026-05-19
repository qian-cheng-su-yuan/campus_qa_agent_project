# PyCharm 小白运行指南

## 1. 打开项目

解压项目后，在 PyCharm 中选择 `File -> Open`，打开 `campus_qa_agent_project` 文件夹。

## 2. 创建虚拟环境

打开 PyCharm 底部 Terminal，输入：

```bash
python -m venv .venv
```

Windows：

```bash
.venv\Scripts\activate
```

## 3. 安装依赖

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 4. 配置 API Key

复制 `.env.example` 为 `.env`，然后填写你的 Key。

Windows：

```bash
copy .env.example .env
```

## 5. 启动后端

```bash
python run_api.py
```

看到类似下面内容说明成功：

```text
Uvicorn running on http://127.0.0.1:8000
```

## 6. 启动前端

再打开一个新的 Terminal：

```bash
python run_web.py
```

打开浏览器：

```text
http://127.0.0.1:8501
```

## 7. 常见问题

### 后端未连接

先确认 `python run_api.py` 是否正在运行。

### API Key 不生效

修改 `.env` 后需要重启后端。

### 依赖安装慢

使用清华镜像：

```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```
