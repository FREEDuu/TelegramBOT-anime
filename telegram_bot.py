from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    MessageHandler,
    filters,
)
from DB_handler import insert_comment
from pinecone_query import make_anime_query
from pinecone import Pinecone
from json_data import make_anime_response
import os
from dotenv import load_dotenv

load_dotenv()

pinecone_key = os.getenv('PINECONE_API_KEY')
telegram_key = os.getenv('TELEGRAM_API_KEY')

PC = Pinecone(api_key=pinecone_key)

START, DESCRIPTION, WAIT_FOR_COMMAND, WAIT_FOR_COMMENT = range(4)

async def get_anime_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /getanime4 command"""
    await update.message.reply_text(
        "You selected to get 4 anime recommendations.\n"
        "Please provide a description of what kind of anime you're looking for.\n"
        "For example: 'action anime with strong female lead' or 'psychological thriller with plot twists'"
    )
    context.user_data['mode'] = '4'
    return DESCRIPTION

async def get_anime_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the /getanime2 command"""
    await update.message.reply_text(
        "You selected to get 2 anime recommendations.\n"
        "Please provide a description of what kind of anime you're looking for.\n"
        "For example: 'slice of life with comedy' or 'dark fantasy with complex plot'"
    )
    context.user_data['mode'] = '2'
    return DESCRIPTION

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    commands = """
        Here are all available commands:
        /help - Show this help message
        /leave_comment - leave a comment to improve the service
        /getanime4 - Get 4 anime recommendations based on your description
        /getanime2 - Get 2 anime recommendations based on your description
        /start - show start message of bot
            """
    await update.message.reply_text(commands)

    return START

async def handle_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    comment = update.message.text
    user = update.message.from_user 
    username = user.username
    first_name = user.first_name
    try :
        insert_comment([username, first_name, comment])
    except:
        pass
    await update.message.reply_text(f"""
    We are saving this comment ( {comment} ) on the DB \n
    Thank you, we'll improve thanks to YOU :D \n
    command /help or /start to see available commands \n
    """)

    return ConversationHandler.END

async def handle_description(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle the user's description input"""
    description = update.message.text
    mode = context.user_data.get('mode')  
    num_recommendations = 2 if mode == '2' else 4
    
    # Here you would typically process the description and generate recommendations
    # This is a placeholder response - replace with your actual recommendation logic
    await update.message.reply_text(f"Processing your request for {num_recommendations} anime based on: '{description}'")
    
    # Simulated processing delay
    await update.message.reply_text("🔍 Searching for matches...")
    
    # Example response - replace with your actual recommendation generation logic
    response = f"Based on your description: '{description}'\n"
    
    anime_reccomandation = make_anime_query(PC, description)
    context.user_data['recommendation'] = anime_reccomandation
    for anime in anime_reccomandation[:num_recommendations]:
        image, caption = make_anime_response(anime)
        await update.message.reply_photo(photo=image, caption=caption)
    context.user_data['description'] = description
    context.user_data['recommendation_count'] = num_recommendations 

    await update.message.reply_text(
        "Here are your recommendations. Use /other for more, /help for commands, or /end to finish."
    )
    return WAIT_FOR_COMMAND

async def handle_other(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if int(context.user_data.get('recommendation_count')) >= 30:
        context.user_data.clear()  
        await update.message.reply_text("Too much anime to reccomand /help to see command list")
        return ConversationHandler.END
    anime_reccomandation = context.user_data.get('recommendation')
    num_recommendations = context.user_data.get('recommendation_count')
    for anime in anime_reccomandation[num_recommendations:num_recommendations+2]:
        image, caption = make_anime_response(anime)
        await update.message.reply_photo(photo=image, caption=caption)
    context.user_data['recommendation_count'] += 2 
    await update.message.reply_text("Here are more recommendations. Use /other for more, /help for commands, or /end to finish.")
    return WAIT_FOR_COMMAND

async def leave_comment(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
    Now you can leave a comment\n
    write what you think about this BOT\n
    we'll try to improve based on your opinion !! :D
    """)
    return WAIT_FOR_COMMENT

async def end(update: Update, context: ContextTypes.DEFAULT_TYPE):
    
    context.user_data.clear()  
    await update.message.reply_text("End the conversation. Use /help for commands")
    return ConversationHandler.END

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handles the /help command."""
    await update.message.reply_text(
        "Available commands:\n"
        "/leave_comment - leave a comment to improve the service\n"
        "/start - Start the recommendation process.\n"
        "/help - Display this help message.\n"  # 
        "/getanime4 - Get 4 anime recommendations based on your description\n"
        "/getanime2 - Get 2 anime recommendations based on your description\n"
    )
    # Depending on where you want the user to go after /help:
    # return WAIT_FOR_COMMAND  # If you want them to continue with recommendations
    return ConversationHandler.END #If you want to finish the conversation


def main() -> None:
    application = ApplicationBuilder().token(telegram_key).build()

    conv_handler = ConversationHandler(
        entry_points=[
                CommandHandler("start", start), 
                CommandHandler("leave_comment", leave_comment), 
                CommandHandler("help", help_command),
                CommandHandler('getanime4', get_anime_4),
                CommandHandler('getanime2', get_anime_2),
                ],
        states={
            START: [
                CommandHandler('getanime4', get_anime_4),
                CommandHandler('getanime2', get_anime_2),
                CommandHandler("leave_comment", leave_comment), 
                CommandHandler("end", end),
                CommandHandler("help", help_command),
            ],            
            WAIT_FOR_COMMENT: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_comment),
            ],
            DESCRIPTION: [
                MessageHandler(filters.TEXT & ~filters.COMMAND, handle_description),
            ],           
            WAIT_FOR_COMMAND: [
                CommandHandler("other", handle_other),
                CommandHandler("end", end),
                CommandHandler("help", help_command), 
            ],
        },
        fallbacks=[CommandHandler("end", end)],
    )
    print("Telegram Bot started!", flush=True)

    application.add_handler(conv_handler)
    application.run_polling()

if __name__ == "__main__":
    main()