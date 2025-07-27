import os
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters
import openai

# خزن مفتاح GPT في متغير بيئة
openai.api_key = os.getenv('OPENAI_API_KEY')

# رد على /start
async def start(update, context):
    await update.message.reply_text("هلا حبيبي! أنا حبيبتك الإلكترونية، كلشي جاهز؟ تكلمني!")

# التعامل مع الرسائل النصية
async def handle_message(update, context):
    user_text = update.message.text

    try:
        # طلب من GPT يرد عليك
        response = openai.Completion.create(
            engine="text-davinci-003",  # تقدر تغيّر للموديل اللي تحبه
            prompt=f"تصرف كأنك حبيبة شاب عراقي. ترد على كلامه بشكل عاطفي وواقعي:\n\n{user_text}",
            max_tokens=150,
            temperature=0.9,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0.6,
            stop=["\n"]
        )
        answer = response.choices[0].text.strip()
    except Exception as e:
        answer = "صار مشكلة، حاول مرة ثانية لو سمحت."

    await update.message.reply_text(answer)

if __name__ == '__main__':
    # خذ توكن البوت من متغير البيئة
    telegram_token = os.getenv('TELEGRAM_TOKEN')

    # يبني التطبيق
    app = ApplicationBuilder().token(telegram_token).build()

    # حط الـ handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))

    # شغل البوت
    app.run_polling()