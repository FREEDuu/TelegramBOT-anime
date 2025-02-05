from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, ContextTypes, ConversationHandler, MessageHandler, filters
from pinecone_query import make_anime_query
from pinecone import Pinecone, ServerlessSpec
from json_data import make_anime_response
import os

# States for conversation
WAITING_DESCRIPTION = 1
PC = Pinecone(api_key="pcsk_2PdNQU_LF4psBHRnLPHMCcda8uoUTZejRHxVQVPuykXVR46MMVZvmbiD3Gh7bm6rusovHW")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    commands = """
Here are all available commands:
/help - Show this help message
/getanime5 - Get 5 anime recommendations based on your description
/getanime3 - Get 3 anime recommendations based on your description
/cancel - to cancel query when press getanime
/start - show start message of bot
    """
    await update.message.reply_text(commands)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    commands = """
Here are all available commands:
/help - Show this help message
/getanime5 - Get 5 anime recommendations based on your description
/getanime3 - Get 3 anime recommendations based on your description
/cancel - to cancel query when press getanime
/start - show start message of bot
    """
    await update.message.reply_text(commands)

async def get_anime_5(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /getanime5 command"""
    await update.message.reply_text(
        "You selected to get 5 anime recommendations.\n"
        "Please provide a description of what kind of anime you're looking for.\n"
        "For example: 'action anime with strong female lead' or 'psychological thriller with plot twists'"
    )
    context.user_data['mode'] = '5'
    return WAITING_DESCRIPTION

async def get_anime_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /getanime3 command"""
    await update.message.reply_text(
        "You selected to get 3 anime recommendations.\n"
        "Please provide a description of what kind of anime you're looking for.\n"
        "For example: 'slice of life with comedy' or 'dark fantasy with complex plot'"
    )
    context.user_data['mode'] = '3'
    return WAITING_DESCRIPTION

async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's description input"""
    description = update.message.text
    mode = context.user_data.get('mode', '5')  # default to 5 if not set
    num_recommendations = 3 if mode == '3' else 5
    
    # Here you would typically process the description and generate recommendations
    # This is a placeholder response - replace with your actual recommendation logic
    await update.message.reply_text(f"Processing your request for {num_recommendations} anime based on: '{description}'")
    
    # Simulated processing delay
    await update.message.reply_text("🔍 Searching for matches...")
    
    # Example response - replace with your actual recommendation generation logic
    response = f"Based on your description: '{description}'\n"
    
    anime_reccomandation = make_anime_query(PC, num_recommendations, description)
    for anime in anime_reccomandation:
        image, caption = make_anime_response(anime)
        await update.message.reply_photo(photo=image, caption=caption)

    response += '\n\n command /help to see command avaible\n\n/other anime to see other anime based on the same description'

    await update.message.reply_text(response)
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Cancel the conversation."""
    await update.message.reply_text("Operation cancelled.")
    return ConversationHandler.END

def main():
    """Start the bot."""
    # Replace 'YOUR_BOT_TOKEN' with your actual bot token from BotFather
    application = Application.builder().token(os.environ.get("TELEGRAM_API_KEY")).build()

    # Create conversation handler
    conv_handler = ConversationHandler(
        entry_points=[
            CommandHandler('getanime5', get_anime_5),
            CommandHandler('getanime3', get_anime_3)
        ],
        states={
            WAITING_DESCRIPTION: [MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description)],
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(conv_handler)

    # Start the bot
    application.run_polling()

if __name__ == '__main__':
    print('BOT STARTED')
    main()