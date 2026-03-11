import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# استلام المفاتيح من Render (طريقة آمنة)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا Ones AI، كيف أخدمك يا مهندس؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        res = model.generate_content(update.message.text)
        await update.message.reply_text(res.text)
    except Exception as e:
        print(f"Error: {e}")
        await update.message.reply_text("أنا متصل، لكن هناك ضغط بسيط. جرب مرة أخرى!")

if __name__ == '__main__':
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()
