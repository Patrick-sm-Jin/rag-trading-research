# main.py

import argparse
from ingestor import ingest
from chatbot import ask, chat

def main():
    parser = argparse.ArgumentParser(description="RAG 트레이딩 리서치봇")
    parser.add_argument(
        "--mode",
        choices=["ingest", "ask", "chat"],
        default="chat",
        help="ingest: 문서 저장 / ask: 1회 질문 / chat: 대화 모드"
    )
    parser.add_argument(
        "--question",
        type=str,
        help="--mode ask 일 때 질문 입력",
        default=""
    )
    args = parser.parse_args()

    if args.mode == "ingest":
        print("📂 문서를 벡터DB에 저장합니다...")
        ingest()

    elif args.mode == "ask":
        if not args.question:
            print("⚠️ 질문을 입력해주세요. 예: --question '비트코인 동향은?'")
            return
        ask(args.question)

    elif args.mode == "chat":
        chat()

if __name__ == "__main__":
    main()