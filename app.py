from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from dotenv import load_dotenv
import os
import random

# Load Token
load_dotenv()
TOKEN = os.getenv("TOKEN")

# Topics Data
topics = {
    "Basics": [
        {"q": "Python kya hai?", "a": "Python ek high-level interpreted language hai."},
        {"q": "List vs Tuple?", "a": "List mutable, Tuple immutable."}
    ],
    "OOP": [
        {"q": "OOP ke 4 pillars?", "a": "Encapsulation, Inheritance, Polymorphism, Abstraction"},
        {"q": "Inheritance kya hai?", "a": "Ek class dusri class ke properties inherit karti hai."}
    ],
    "Flask": [
        {"q": "Flask kya hai?", "a": "Python ka lightweight web framework."},
        {"q": "Routing kya hai?", "a": "URL ko function se connect karna."}
    ],
    "DSA": [
        {"q": "Stack kya hai?", "a": "LIFO structure (Last In First Out)."},
        {"q": "Queue kya hai?", "a": "FIFO structure (First In First Out)."}
    ]
}

quiz_data = [
    {"q": "Python creator?\nA. Dennis\nB. Guido\nC. James", "ans": "B"},
    {"q": "Tuple type?\nA. Mutable\nB. Immutable", "ans": "B"}
]

user_state = {}

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["Basics", "OOP"], ["Flask", "DSA"], ["Quiz"]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    await update.message.reply_text(
        "👋 Welcome to Advanced Interview Bot\n\nSelect Topic:",
        reply_markup=reply_markup
    )

# Handle Topic Selection
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user.id

    # Topic Questions
    if text in topics:
        q = random.choice(topics[text])
        user_state[user] = q
        await update.message.reply_text(f"❓ {q['q']}\n\nType 'answer' to see answer\nType 'next' for next question")

    # Answer
    elif text.lower() == "answer":
        if user in user_state:
            await update.message.reply_text(f"✅ {user_state[user]['a']}")
        else:
            await update.message.reply_text("Topic select karo pehle")

    # Next Question
    elif text.lower() == "next":
        if user in user_state:
            topic = None
            for t in topics:
                if user_state[user] in topics[t]:
                    topic = t
                    break
            q = random.choice(topics[topic])
            user_state[user] = q
            await update.message.reply_text(f"❓ {q['q']}")
        else:
            await update.message.reply_text("Pehle topic select karo")

    # Quiz Start
    elif text == "Quiz":
        q = random.choice(quiz_data)
        user_state[user] = q
        await update.message.reply_text(f"📝 {q['q']}\n\nReply A/B/C")

    # Quiz Answer
    elif text.upper() in ["A", "B", "C"]:
        if user in user_state and "ans" in user_state[user]:
            if text.upper() == user_state[user]["ans"]:
                await update.message.reply_text("🎉 Correct!")
            else:
                await update.message.reply_text(f"❌ Wrong! Answer: {user_state[user]['ans']}")
        else:
            await update.message.reply_text("Start quiz first")

    else:
        await update.message.reply_text("Invalid option 😅")

# App
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("🚀 Bot Running...")
app.run_polling()