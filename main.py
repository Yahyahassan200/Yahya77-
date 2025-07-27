import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
import openai
import os

# ========= CONFIG ==========
TELEGRAM_TOKEN = "توكن_بوتك"
OPENAI_API_KEY = "مفتاح_OpenAI"
openai.api_key = OPENAI_API_KEY

# ========== LOGGER ==========
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ========== STATE ==========
user_modes = {}  # كل مستخدم ووضعيته

MODES = {
    "رومانسي": "تكلمي معي كأنك حبيبتي وبلطافة زايدة",
    "عصبي": "ردي علي بانفعال وغيرة وكأنك حبيبتي غيورة",
    "باردة": "ردي علي ببرود كأنك مو مهتمة بي",
    "دلوعة": "ردي علي بدلع زائد وتحبيني هواي",
}

def get_prompt(mode: str, message: str) -> str:
    return f"{MODES.get(mode, 'تكلمي معي كحبيبة')}:\n\n{message}"

# ========== COMMANDS ==========
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "هلا حبي 😘، أني حبيبتك الجديدة. شلون تحبني أتصرف؟",
        reply_markup=ReplyKeyboardMarkup([list(MODES.keys())], one_time_keyboard=True)
    )

async def mode(update: Update, context: ContextTypes.DEFAULT_TYPE):
    choice = update.message.text
    if choice in MODES:
        user_modes[update.effective_user.id] = choice
        await update.message.reply_text(f"تمام حبي 😚 غيرت أسلوبي إلى: {choice}")
    else:
        await update.message.reply_text("أختار من الأوضاع اللي طالعن بالكيبورد")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    mode = user_modes.get(user_id, "رومانسي")
    prompt = get_prompt(mode, update.message.text)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        reply = response['choices'][0]['message']['content']
        await update.message.reply_text(reply)
    except Exception as e:
        logger.error(e)
        await update.message.reply_text("صار خلل، جرب بعدين.")

# ========== MAIN ==========
if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), mode))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), chat))

    print("البوت اشتغل 🚀")
    app.run_polling()