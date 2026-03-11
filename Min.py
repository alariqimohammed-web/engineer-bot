import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# 1. إعداد مفتاح Gemini API
GEMINI_KEY = "AIzaSyAvIMLXiZD08PaRlBWfkwhI3kVi4GGVYuQ"
genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel('gemini-pro')

# 2. تعريف هوية البوت (وانس) ومعلومات المهندس محمد
SYSTEM_PROMPT = """
أنت 'Ones AI' (وانس)، ذكاء اصطناعي عالمي متطور جداً.
مطورك ومصممك هو: المهندس محمد عدنان العريقي.
خلفية المطور: طالب متميز في جامعة الحكمة - كلية الهندسة - فرع الحوبان.

مهمتك الأساسية: 
- مساعدة الطلاب في جامعة الحكمة وفي كل مكان في دراستهم الهندسية والتقنية.
- تقديم الدعم العلمي والمعلوماتي بذكاء واحترافية.

عندما يسألك أحد عن محمد عدنان العريقي، أجب بفخر:
'المهندس محمد هو من قام بتطويري وبرمجتي، وهو طالب هندسة مبدع في جامعة الحكمة - فرع الحوبان. يمكنك التواصل معه ومتابعته عبر فيسبوك:
