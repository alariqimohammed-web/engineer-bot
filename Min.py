import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. قسم السيرفر الوهمي (لحل مشكلة Render وتجنب الرسائل الحمراء)
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Ones AI is Running...")

def run_health_check():
    # Render يعطينا بورت تلقائي في الإعدادات، وإذا لم يجده يستخدم 8080
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), HealthCheckHandler)
    server.serve_forever()

# 2. إعداد الذكاء الاصطناعي (Gemini)
# يسحب المفتاح من Environment Variables التي وضعناها في Render
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-pro')

# 3. دالة الترحيب عند الضغط على /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.effective_user.first_name
    await update.message.reply_text(f"أهلاً بك يا بشمهندس {user_name}! أنا Ones AI المطور، كيف أقدر أساعدك اليوم؟")

# 4. دالة معالجة الرسائل والرد بالذكاء الاصطناعي
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # إظهار حالة "جاري الكتابة..." في التيليجرام ليعرف المستخدم أن البوت يعمل
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        
        # إرسال سؤال المستخدم إلى Gemini
        user_text = update.message.text
        response = model.generate_content(user_text)
        
        # التأكد من وجود رد وإرساله
        if response.text:
            await update.message.reply_text(response.text)
        else:
            await update.message.reply_text("عذراً، لم أستطع تكوين إجابة حالياً. جرب صياغة السؤال بشكل آخر.")
            
    except Exception as e:
        print(f"خطأ في Gemini: {e}")
        await update.message.reply_text("أنا معك، لكن يبدو أن هناك مشكلة في الاتصال بمحرك الذكاء الاصطناعي. جرب مرة أخرى بعد لحظات.")

# 5. تشغيل البوت
if __name__ == '__main__':
    # تشغيل السيرفر الوهمي في "خلفية" الكود
    threading.Thread(target=run_health_check, daemon=True).start()
    
    # سحب توكن التيليجرام من Render
    TOKEN = os.environ.get("TELEGRAM_TOKEN")
    
    if not TOKEN:
        print("خطأ: لم يتم العثور على TELEGRAM_TOKEN في الإعدادات!")
    else:
        app = ApplicationBuilder().token(TOKEN).build()
        
        # إضافة الأوامر والمستقبلات
        app.add_handler(CommandHandler('start', start))
        app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
        
        print("--- البوت الآن يعمل عالمياً (LIVE) ---")
        app.run_polling()
