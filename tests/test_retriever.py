from app.services.retriever import SimpleRetriever
from app.services.text_splitter import TextChunk


def test_retriever_can_find_related_chunk():
    retriever = SimpleRetriever()
    chunks = [
        TextChunk(source="leave.txt", chunk_id=1, content="学生请假需要提交请假申请表和医院证明。"),
        TextChunk(source="library.txt", chunk_id=2, content="图书馆普通图书可以借阅三十天。"),
    ]
    retriever.build(chunks)
    results = retriever.search("请假需要什么材料", top_k=1)
    assert results
    assert results[0].source == "leave.txt"
