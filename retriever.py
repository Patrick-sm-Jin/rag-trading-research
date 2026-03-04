# retriever.py

from ingestor import load_vectorstore
from config import TOP_K

def get_retriever():
    """벡터DB에서 검색기 생성"""
    vectorstore = load_vectorstore()
    if not vectorstore:
        return None

    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": TOP_K},
    )
    return retriever

def search(query: str) -> list:
    """쿼리와 관련된 문서 검색"""
    retriever = get_retriever()
    if not retriever:
        return []

    docs = retriever.invoke(query)
    print(f"\n🔍 검색 결과 ({len(docs)}개):")
    for i, doc in enumerate(docs, 1):
        print(f"{i}. {doc.page_content[:100]}...")

    return docs