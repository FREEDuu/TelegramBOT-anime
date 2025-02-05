from telegram.ext import Application, CommandHandler, MessageHandler, filters
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from utils.api import get_casual_anime
from dotenv import load_dotenv
import os   

load_dotenv()

TOKEN = os.getenv('token')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    commands = [
        "/help - Show all available commands",
        "/get_anime - Get a random anime recommendation"
    ]
    
    help_text = "Available commands:\n" + "\n".join(commands)
    await update.message.reply_text(help_text)

async def get_anime(update: Update, context: ContextTypes.DEFAULT_TYPE):

    image, caption = get_casual_anime()
    chat_id = update.message.chat.id
    await update.message.reply_photo(photo=image, caption=caption)

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user_first_name = update.message.from_user.first_name
    welcome_message = f"""Welcome {user_first_name}! 👋
I'm your Anime Bot. Use /help to see all available commands."""
    await update.message.reply_text(welcome_message)


def main():
    """
    Handles the initial launch of the program (entry point).
    """
    token = TOKEN
    application = Application.builder().token(token).concurrent_updates(True).read_timeout(30).write_timeout(30).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("get_anime", get_anime))
    print("Telegram Bot started!", flush=True)
    application.run_polling()

if __name__ == '__main__':
    main()
