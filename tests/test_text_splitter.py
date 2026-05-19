from app.services.document_loader import RawDocument
from app.services.text_splitter import TextSplitter


def test_split_documents():
    splitter = TextSplitter(chunk_size=20, chunk_overlap=5)
    docs = [RawDocument(source="demo.txt", content="学生请假需要提交申请表和证明材料。返校后需要及时销假。")]
    chunks = splitter.split_documents(docs)
    assert len(chunks) >= 1
    assert chunks[0].source == "demo.txt"
