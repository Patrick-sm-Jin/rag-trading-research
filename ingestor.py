# ingestor.py
import os
from langchain_community.document_loaders import (
    TextLoader,
    CSVLoader,
    DirectoryLoader,
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_anthropic import ChatAnthropic
from langchain_community.embeddings import HuggingFaceEmbeddings
from config import (
    ANTHROPIC_API_KEY,
    VECTORSTORE_PATH,
    DATA_PATH,
    CHUNK_SIZE,
    CHUNK_OVERLAP,
)

def get_embeddings():
    """임베딩 모델 로드 (무료 HuggingFace 사용)"""
    return HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

def load_documents():
    """data/ 폴더에서 문서 로드"""
    documents = []

    # txt 파일 로드
    txt_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.txt",
        loader_cls=TextLoader,
        silent_errors=True,
    )
    documents.extend(txt_loader.load())

    # csv 파일 로드 (매매기록)
    csv_loader = DirectoryLoader(
        DATA_PATH,
        glob="**/*.csv",
        loader_cls=CSVLoader,
        silent_errors=True,
    )
    documents.extend(csv_loader.load())

    print(f"[로드 완료] 총 {len(documents)}개 문서")
    return documents

def ingest():
    """문서 → 청크 분할 → 벡터DB 저장"""
    print("📂 문서 로드 중...")
    documents = load_documents()

    if not documents:
        print("⚠️ data/ 폴더에 문서가 없어요! txt 또는 csv 파일을 넣어주세요.")
        return None

    print("✂️ 청크 분할 중...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE,
        chunk_overlap=CHUNK_OVERLAP,
    )
    chunks = splitter.split_documents(documents)
    print(f"[분할 완료] {len(chunks)}개 청크")

    print("🔢 벡터DB 저장 중...")
    embeddings = get_embeddings()
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=VECTORSTORE_PATH,
    )
    print(f"[저장 완료] 벡터DB: {VECTORSTORE_PATH}")
    return vectorstore


def load_vectorstore():
    """기존 벡터DB 로드"""
    if not os.path.exists(VECTORSTORE_PATH):
        print("⚠️ 벡터DB가 없어요! ingest()를 먼저 실행해주세요.")
        return None

    embeddings = get_embeddings()
    vectorstore = Chroma(
        persist_directory=VECTORSTORE_PATH,
        embedding_function=embeddings,
    )
    print("[벡터DB 로드 완료]")
    return vectorstore