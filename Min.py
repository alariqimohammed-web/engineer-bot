import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. إعداد مفتاح Gemini API
GEMINI_KEY = "AIzaSyAvIMLXiZD08PaRlBWfkwhI3kVi4GGVYuQ"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# 2. تعريف هوية البوت
SYSTEM_PROMPT = """
أنت 'Ones AI' (وانس)، ذكاء اصطناعي عالمي متطور. مطورك هو المهندس محمد عدنان العريقي، طالب بجامعة الحكمة - كلية الهندسة - فرع الحوبان. رابط فيسبوك المطور: https://www.facebook.com/share/17Qrgq6qoR/
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"مرحباً {user_name}! أنا Ones AI، المساعد الذكي للمهندس محمد عدنان العريقي. كيف أساعدك اليوم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    full_prompt = f"{SYSTEM_PROMPT}\nالمستخدم يسأل: {user_input}"
    try:
        response = model.generate_content(full_prompt)
        await update.message.reply_text(response.text)
    except:
        await update.message.reply_text("حدث خطأ بسيط، حاول مرة أخرى!")

if __name__ == '__main__':
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if TOKEN:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        application.run_polling()
