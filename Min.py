import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. سيرفر وهمي لإبقاء البوت متصلاً (Health Check)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Ones AI is Online")

def run_health_check():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 2. إعداد Gemini (استخدام الموديل السريع 1.5 Flash)
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
# أضفنا تعليمات للنظام ليكون البوت ذكياً جداً
model = genai.GenerativeModel(
    model_name='gemini-1.5-flash',
    generation_config={"temperature": 0.7}
)

# 3. دالة الترحيب
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"أهلاً بك يا مبرمج محمد! أنا Ones AI، جاهز أتكلم معك في أي موضوع. ايش في بالك؟")

# 4. دالة معالجة الرسائل (الذكاء الكامل)
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # إشعار "يتم الكتابة" ليظهر في تلجرام
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # إرسال النص لـ Gemini
        user_text = update.message.text
        response = model.generate_content(user_text)
        
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("عذراً يا هندسة، السؤال يحتاج صياغة تانية.")
            
    except Exception as e:
        print(f"Error: {e}")
        # إذا حصل خطأ، هذا يعني أن المفتاح الجديد لسه ما اشتغل أو فيه ضغط
        await update.message.reply_text("أنا أسمعك، لكن Gemini لسه ما رد. جرب ترسل الرسالة مرة ثانية الآن.")

# 5. تشغيل البوت
if __name__ == '__main__':
    threading.Thread(target=run_health_check, daemon=True).start()
    
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    if TOKEN:
        app = ApplicationBuilder().token(TOKEN).build()
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("--- البوت شغال الآن بأحدث موديل ---")
        app.run_polling()
