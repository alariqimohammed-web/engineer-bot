import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

# تشغيل سيرفر وهمي لإرضاء موقع Render
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is Running")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# إعداد Gemini
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا Ones AI، كيف أخدمك يا مهندس محمد؟")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # إرسال حالة "يتم الكتابة" ليشعر المستخدم بالسرعة
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        res = model.generate_content(update.message.text)
        await update.message.reply_text(res.text)
    except Exception as e:
        await update.message.reply_text("أنا معك، لكن يبدو أن هناك ضغطاً بسيطاً في الخدمة، حاول مرة أخرى!")

if __name__ == '__main__':
    # بدء السيرفر الوهمي في خلفية الكود
    threading.Thread(target=run_health_check, daemon=True).start()
    
    # تشغيل البوت
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("Ones AI is now LIVE!")
    app.run_polling()
