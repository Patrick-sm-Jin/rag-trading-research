# 🤖 RAG 트레이딩 리서치봇

> 내 매매 기록과 뉴스 데이터를 기반으로 Claude AI가 트레이딩 인사이트를 제공하는 RAG(Retrieval Augmented Generation) 챗봇

![Python](https://img.shields.io/badge/Python-3.11+-blue?style=flat-square&logo=python)
![Claude AI](https://img.shields.io/badge/Claude-AI-orange?style=flat-square)
![LangChain](https://img.shields.io/badge/LangChain-🦜-green?style=flat-square)
![ChromaDB](https://img.shields.io/badge/ChromaDB-Vector_DB-purple?style=flat-square)

---

## 📌 프로젝트 개요

자율 트레이딩 시스템 포트폴리오의 일환으로 제작된 RAG 기반 리서치봇입니다.
매매 기록, 뉴스 데이터를 벡터DB에 저장하고 자연어 질문으로 트레이딩 인사이트를 얻을 수 있습니다.

### 🔗 트레이딩 시스템과의 연결
```
P1 자동매매 → P2 자동기록 → P3 자동분석
                    ↓
            RAG 리서치봇 (현재)
            매매기록 + 뉴스 기반 AI 분석
                    ↓
            P4 전략 최적화에 인사이트 활용
```

---

## ✨ 주요 기능

- **문서 자동 인제스트** — 매매기록(CSV), 뉴스(TXT) 등을 벡터DB에 자동 저장
- **시맨틱 검색** — 질문과 관련된 데이터를 벡터 유사도로 검색
- **AI 트레이딩 분석** — Claude AI가 데이터 기반으로 트레이더 관점 답변 생성
- **대화형 챗봇** — 터미널에서 자연어로 질문 가능

---

## 🛠 기술 스택

| 분류 | 기술 |
|------|------|
| 언어 | Python 3.11+ |
| AI | Anthropic Claude API |
| RAG 프레임워크 | LangChain |
| 벡터DB | ChromaDB |
| 임베딩 | HuggingFace sentence-transformers |

---

## 📁 프로젝트 구조

```
rag-trading-research/
├── main.py          # 실행 진입점 (ingest / ask / chat 모드)
├── config.py        # API 키 및 설정 (⚠️ gitignore 처리)
├── ingestor.py      # 문서 → 청크 분할 → 벡터DB 저장
├── retriever.py     # 벡터DB 시맨틱 검색
├── chatbot.py       # Claude AI 답변 생성
├── data/            # 매매기록, 뉴스 데이터 (⚠️ gitignore 처리)
└── vectorstore/     # ChromaDB 벡터DB (⚠️ gitignore 처리)
```

---

## ⚙️ 설치 및 실행

### 1. Python 버전 확인 (3.11 권장)
```bash
python3 --version
```

### 2. 가상환경 생성
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. 패키지 설치
```bash
pip install langchain langchain-community langchain-anthropic langchain-chroma langchain-text-splitters chromadb anthropic sentence-transformers
```

### 4. config.py 설정
```python
# config.py
ANTHROPIC_API_KEY = "your_claude_api_key"
VECTORSTORE_PATH  = "./vectorstore"
DATA_PATH         = "./data"
CHUNK_SIZE        = 500
CHUNK_OVERLAP     = 50
TOP_K             = 3
CLAUDE_MODEL      = "claude-opus-4-6"
MAX_TOKENS        = 1000
```

> ⚠️ `config.py` 는 `.gitignore` 에 추가하여 API 키가 GitHub에 노출되지 않도록 합니다.

### 5. 데이터 추가
`data/` 폴더에 매매기록(CSV) 또는 뉴스(TXT) 파일을 추가합니다.

```
data/
├── trading_log.csv   # 매매 기록
└── news.txt          # 뉴스 데이터
```

### 6. 실행

**문서를 벡터DB에 저장**
```bash
python3 main.py --mode ingest
```

**1회 질문**
```bash
python3 main.py --mode ask --question "BTC 매매 결과는 어땠어?"
```

**대화 모드**
```bash
python3 main.py --mode chat
```

---

## 💬 사용 예시

```
🤖 RAG 트레이딩 리서치봇
종료하려면 'quit' 입력

❓ 질문: BTC 매매 결과는 어땠어?

🔍 검색 결과 (3개):
1. 2026-03-01 BTC 매수 진입가 85000달러...

🤖 Claude 답변:
# BTC 매매 결과 요약
BTC 2건 모두 수익 마감, 합산 수익률 +5.2%
...
```

---

## 🗺 로드맵

- [x] 문서 벡터DB 저장 (CSV, TXT)
- [x] 시맨틱 검색
- [x] Claude AI 트레이딩 분석
- [x] 대화형 챗봇 모드
- [ ] 뉴스 큐레이션봇 연동 (자동 뉴스 저장)
- [ ] 텔레그램 봇 연동
- [ ] P4 전략 최적화에 인사이트 활용

---

## 🔗 관련 프로젝트

> 자율 트레이딩 시스템 포트폴리오의 일부입니다.

| 프로젝트 | 상태 |
|---------|------|
| P1 자동매매 시스템 | ✅ 완료 |
| P2 자동 기록 시스템 | ✅ 완료 |
| P3 자동 데이터 분석 | ✅ 완료 |
| P4 전략 자동 최적화 | 🔄 진행 중 |
| P5 리스크 관리 & 경보 | 📋 계획 |
| 뉴스 큐레이션 봇 | ✅ 완료 |
| **RAG 트레이딩 리서치봇** | ✅ 완료 |
