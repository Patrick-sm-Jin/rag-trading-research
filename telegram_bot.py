# telegram_bot.py

import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from chatbot import ask
from config import ANTHROPIC_API_KEY, TELEGRAM_BOT_TOKEN

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """봇 시작 메시지"""
    await update.message.reply_text(
        "🤖 *RAG 트레이딩 리서치봇*\n\n"
        "매매 기록과 뉴스 데이터를 기반으로 질문에 답해드려요!\n\n"
        "예시 질문:\n"
        "• BTC 매매 결과는 어땠어?\n"
        "• 최근 손실 패턴이 뭐야?\n"
        "• 오늘 시장 뉴스 요약해줘",
        parse_mode="Markdown"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """메시지 수신 → RAG 답변"""
    question = update.message.text

    print(f"[질문 수신] {question}")

    # 로딩 메시지
    loading_msg = await update.message.reply_text("🔍 분석 중...")

    try:
        # RAG 답변 생성
        answer = ask(question)

        await loading_msg.delete()

        # 섹션별로 나눠서 발송
        sections = {
            "[핵심답변]"      : "📌 *핵심 답변*",
            "[수치근거]"      : "📊 *수치 근거*",
            "[트레이더인사이트]": "💡 *트레이더 인사이트*",
        }

        sent = False
        for key, title in sections.items():
            if key in answer:
                start = answer.find(key) + len(key)
                next_keys = [k for k in sections.keys() if k != key]
                ends = [answer.find(k) for k in next_keys if answer.find(k) > start]
                end = min(ends) if ends else len(answer)
                content = answer[start:end].strip()
                if content:
                    await update.message.reply_text(
                        f"{title}\n\n{content}",
                        parse_mode="Markdown"
                    )
                    sent = True

        # 섹션 구분자가 없으면 전체 발송
        if not sent:
            await update.message.reply_text(
                f"🤖 *AI 분석 결과*\n\n{answer}",
                parse_mode="Markdown"
            )

    except Exception as e:
        await loading_msg.delete()
        await update.message.reply_text(f"⚠️ 오류가 발생했어요: {e}")
        print(f"[오류]: {e}")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """도움말"""
    await update.message.reply_text(
        "📋 *사용 가능한 명령어*\n\n"
        "/start — 봇 시작\n"
        "/help — 도움말\n"
        "/ingest — 데이터 새로고침\n\n"
        "그냥 질문을 입력하면 RAG가 답해드려요!",
        parse_mode="Markdown"
    )

async def ingest_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """데이터 새로고침"""
    from ingestor import ingest
    await update.message.reply_text("📂 데이터 새로고침 중...")
    try:
        ingest()
        await update.message.reply_text("✅ 데이터 새로고침 완료!")
    except Exception as e:
        await update.message.reply_text(f"⚠️ 오류: {e}")


def main():
    """텔레그램 봇 실행"""
    print("🤖 RAG 텔레그램 봇 시작!")
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    # 핸들러 등록
    app.add_handler(CommandHandler("start",  start))
    app.add_handler(CommandHandler("help",   help_command))
    app.add_handler(CommandHandler("ingest", ingest_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ 봇 실행 중 — 종료하려면 Ctrl+C")
    app.run_polling()


if __name__ == "__main__":
    main()