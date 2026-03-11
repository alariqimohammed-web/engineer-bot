import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. إعداد Gemini
genai.configure(api_key="AIzaSyAvIMLXiZD08PaRlBWfkwhI3kVi4GGVYuQ")
model = genai.GenerativeModel('gemini-pro')

# 2. الهوية (تم مسح الاقتباسات الثلاثية وتعديلها لتعمل بوضوح)
SYSTEM_PROMPT = "أنت Ones AI (وانس)، ذكاء اصطناعي مطورك المهندس محمد عدنان العريقي من جامعة الحكمة فرع الحوبان."

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("مرحباً! أنا Ones AI، المساعد الذكي للمهندس محمد عدنان العريقي. كيف يمكنني مساعدتك اليوم؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_input = update.message.text
        res = model.generate_content(SYSTEM_PROMPT + "\nالمستخدم: " + user_input)
        await update.message.reply_text(res.text)
    except Exception as e:
        await update.message.reply_text("أنا مستيقظ، لكن حدث خطأ بسيط في الاتصال. جرب مرة أخرى!")

if __name__ == '__main__':
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if TOKEN:
        application = ApplicationBuilder().token(TOKEN).build()
        application.add_handler(CommandHandler('start', start))
        application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        application.run_polling()
