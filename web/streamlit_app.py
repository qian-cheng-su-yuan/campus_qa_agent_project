import requests
import streamlit as st

from app.core.config import settings

API_BASE = f"http://{settings.api_host}:{settings.api_port}/api/v1"

st.set_page_config(
    page_title="校园智能问答助手",
    page_icon="🎓",
    layout="wide",
)

st.title("🎓 校园智能问答助手")
st.caption("RAG 知识库问答｜FastAPI 后端｜Streamlit 演示｜支持 API Key 接入")

with st.sidebar:
    st.header("项目状态")
    try:
        health = requests.get(f"{API_BASE}/health", timeout=3).json()
        st.success("后端已连接")
        st.write(f"模型提供方：{health.get('provider')}")
        st.write(f"知识片段数：{health.get('chunk_count')}")
    except Exception:
        st.error("后端未连接")
        st.info("请先运行：python run_api.py")

    st.divider()
    st.header("知识库上传")
    uploaded_files = st.file_uploader(
        "上传校园资料（txt / md / pdf）",
        type=["txt", "md", "pdf"],
        accept_multiple_files=True,
    )
    if st.button("上传并重建知识库", use_container_width=True):
        if not uploaded_files:
            st.warning("请先选择文件")
        else:
            files = []
            for item in uploaded_files:
                files.append(("files", (item.name, item.getvalue(), item.type or "application/octet-stream")))
            try:
                resp = requests.post(f"{API_BASE}/knowledge/upload", files=files, timeout=60)
                resp.raise_for_status()
                st.success(resp.json().get("message", "上传完成"))
            except Exception as exc:
                st.error(f"上传失败：{exc}")

    if st.button("仅重建知识库", use_container_width=True):
        try:
            resp = requests.post(f"{API_BASE}/knowledge/rebuild", timeout=30)
            resp.raise_for_status()
            data = resp.json()
            st.success(f"重建完成：{data['document_count']} 个文档，{data['chunk_count']} 个片段")
        except Exception as exc:
            st.error(f"重建失败：{exc}")

question_examples = [
    "学生请假需要哪些材料？",
    "宿舍水电故障应该怎么报修？",
    "图书馆借书可以借多久？",
    "就业推荐表丢了怎么办？",
    "期末考试缓考怎么申请？",
    "校园卡丢失后怎么补办？",
]

left, right = st.columns([2, 1])

with left:
    st.subheader("智能问答")
    selected = st.selectbox("选择示例问题，也可以自己输入", question_examples)
    question = st.text_area("请输入你的问题", value=selected, height=100)
    top_k = st.slider("检索片段数量", min_value=1, max_value=8, value=settings.default_top_k)

    if st.button("开始提问", type="primary", use_container_width=True):
        if not question.strip():
            st.warning("请输入问题")
        else:
            with st.spinner("正在检索知识库并生成回答..."):
                try:
                    resp = requests.post(
                        f"{API_BASE}/ask",
                        json={"question": question, "top_k": top_k},
                        timeout=90,
                    )
                    resp.raise_for_status()
                    data = resp.json()

                    st.markdown("### 回答")
                    st.write(data["answer"])

                    meta_cols = st.columns(3)
                    meta_cols[0].metric("耗时", f"{data['elapsed_ms']} ms")
                    meta_cols[1].metric("参考片段", len(data["sources"]))
                    meta_cols[2].metric("兜底模式", "是" if data["used_fallback"] else "否")

                    st.markdown("### 参考片段")
                    for idx, item in enumerate(data["sources"], start=1):
                        with st.expander(f"片段 {idx}｜{item['source']}｜score={item['score']}"):
                            st.write(item["content"])
                except Exception as exc:
                    st.error(f"请求失败：{exc}")

with right:
    st.subheader("Agent 工具演示")
    tool_text = st.text_area(
        "输入一段校园通知或制度文本",
        value="学生因病请假需填写请假申请表，提交医院证明，并联系辅导员审批。请假超过三天还需要学院审核。返校后应及时销假。",
        height=180,
    )

    tool = st.radio("选择工具", ["总结", "关键词", "待办清单"], horizontal=True)
    endpoint_map = {
        "总结": "summarize",
        "关键词": "keywords",
        "待办清单": "todo",
    }
    if st.button("运行工具", use_container_width=True):
        try:
            resp = requests.post(
                f"{API_BASE}/tools/{endpoint_map[tool]}",
                json={"text": tool_text},
                timeout=30,
            )
            resp.raise_for_status()
            st.markdown("### 工具结果")
            st.write(resp.json()["result"])
        except Exception as exc:
            st.error(f"工具调用失败：{exc}")

st.divider()
st.caption("面试说明：该项目重点展示 RAG 链路、Prompt 约束、API Key 接入、工程分层和本地演示能力。")
