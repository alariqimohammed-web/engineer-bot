import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# جلب المفاتيح من الإعدادات المخفية (للأمان)
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

SYSTEM_PROMPT = "أنت Ones AI (وانس)، مطورك المهندس محمد عدنان العريقي من جامعة الحكمة."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا Ones AI، كيف يمكنني مساعدتك؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = model.generate_content(f"{SYSTEM_PROMPT}\nالمستخدم: {update.message.text}")
        await update.message.reply_text(res.text)
    except:
        await update.message.reply_text("عذراً، المفتاح معطل أو هناك ضغط. تواصل مع المطور.")

if __name__ == '__main__':
    if TELEGRAM_TOKEN:
        app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        app.run_polling()
