import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# سحب المفاتيح من إعدادات Render (Environment Variables)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
GEMINI_KEY = os.environ.get("GEMINI_API_KEY")

# إعداد الذكاء الاصطناعي
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا ونس، مساعدك الذكي الذي طوره المهندس محمد العريقي. كيف أساعدك اليوم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # إرسال النص لـ Gemini مع هويتك
        prompt = f"أنت اسمك ونس، مساعد ذكي وودود طورك المهندس محمدعدنان العريقي. رد على: {update.message.text}"
        response = model.generate_content(prompt)
        
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Error detail: {e}")
        await update.message.reply_text("أنا أسمعك، لكن يبدو أن هناك ضغط بسيط. أعد إرسال الرسالة الآن.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    print("Bot is running on Render...")
    app.run_polling()
