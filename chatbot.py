# chatbot.py

import anthropic
from retriever import search
from config import ANTHROPIC_API_KEY, CLAUDE_MODEL, MAX_TOKENS

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def ask(question: str) -> str:
    """질문 → 관련 문서 검색 → Claude 답변 생성"""

    print(f"\n❓ 질문: {question}")

    # 1. 관련 문서 검색
    docs = search(question)

    if not docs:
        return "관련 데이터를 찾을 수 없어요. data/ 폴더에 문서를 추가해주세요."

    # 2. 검색된 문서를 컨텍스트로 정리
    context = "\n\n".join([
        f"[문서 {i+1}]\n{doc.page_content}"
        for i, doc in enumerate(docs)
    ])

    # 3. Claude에게 질문
    prompt = f"""아래 데이터를 바탕으로 질문에 답해줘.
트레이더 관점에서 실용적으로 답변해줘.

=== 관련 데이터 ===
{context}

=== 질문 ===
{question}

=== 답변 형식 ===
- 핵심 답변을 먼저 말해줘
- 데이터 근거를 포함해줘
- 투자/트레이딩 관점의 인사이트도 추가해줘
"""

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=MAX_TOKENS,
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response.content[0].text.strip()
    print(f"\n🤖 Claude 답변:\n{answer}")
    return answer


def chat():
    """대화형 챗봇 모드"""
    print("\n" + "="*40)
    print("🤖 RAG 트레이딩 리서치봇")
    print("종료하려면 'quit' 입력")
    print("="*40 + "\n")

    while True:
        question = input("❓ 질문: ").strip()

        if question.lower() in ["quit", "exit", "종료"]:
            print("종료합니다!")
            break

        if not question:
            continue

        ask(question)
        print("\n" + "-"*40 + "\n")