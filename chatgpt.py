import telegram.ext 
from dotenv import load_dotenv
import os
from datetime import time
import pytz
import schedule 
from asyncio.log import logger

# Import Yandex GPT
from langchain_community.llms import YandexGPT 

# Import Telegram modules
from telegram import ParseMode

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')
yandex_api_key = os.getenv('YANDEX_API_KEY')
yandex_model_uri = os.getenv('YANDEX_MODEL_URI')

gpt = YandexGPT(api_key=yandex_api_key, model_uri=yandex_model_uri)

# Define a dictionary to store user ID
user_ids = []

# Define a function to generate news summaries using Yandex GPT
def generate_news_summary():
    # Sample news article
    article = "AI News in Tomsk"

    # Generate a summary of the article using Yandex GPT
    summary = gpt.invoke(article, max_length=100, num_tokens_to_produce=50)

    return summary

# Define a function to send news updates to users
def send_news_update(context):
    summary = generate_news_summary()
    # Send the news update to all subscribers
    for user_id in user_ids:
        context.bot.send_message(user_id, f"📰 *Today's News Update*:\n{summary}", parse_mode=ParseMode.MARKDOWN)

# Define a function to start the bot
def start(update, context):
    user_id = update.effective_user.id
    if user_id not in user_ids:
        user_ids.append(user_id)
    update.message.reply_text("Hello Friend, Welcome. I'm happy to see you!")

# Define a function to stop the bot
def stop(update, context):
    user_id = update.effective_user.id
    if user_id in user_ids:
        user_ids.remove(user_id)
    update.message.reply_text("You will no longer receive news updates from me.")

# Define a function to show help information
def help_command(update, context):
    update.message.reply_text("""
                        Hey there, i'm mangut_bot. Please follow these commands:
                        /start - to start the conversation
                        /stop - to stop receiving news updates
                        /content - information 
                        /contact - contact information 
                        /help - get help menu
                        
                        I hope this helps. 
                        """)

# Define a function to provide content information
def content(update, context):
    update.message.reply_text("""
                       I am an AI News Generator based in Tomsk. I give you 
                       the latest updates of what is happening in Tech in my
                       city as well as global trends.
                        """)

# Define a function to provide contact information
def contact(update, context):
    update.message.reply_text("""
                       I was Developed at the AISiberia Research lab. 
                       If you want to contact us, feel free to call
                       Eniang: +79996198269
                        """)

# Define a function to handle chat messages with the AI
def chatgpt(update, context):
    message = update.message.text
    response = generate_news_summary()  # Using news summary generation for now
    update.message.reply_text(response)

# Define a function to generate news
def generate_news(update, context):
    response = generate_news_summary()
    update.message.reply_text(response)

# Define a function to handle errors
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    updater = telegram.ext.Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    # Add command handlers
    dp.add_handler(telegram.ext.CommandHandler('start', start))
    dp.add_handler(telegram.ext.CommandHandler('stop', stop))
    dp.add_handler(telegram.ext.CommandHandler('help', help_command))
    dp.add_handler(telegram.ext.CommandHandler('content', content))
    dp.add_handler(telegram.ext.CommandHandler('contact', contact))
    dp.add_handler(telegram.ext.MessageHandler(telegram.ext.Filters.text, chatgpt))
    dp.add_handler(telegram.ext.CommandHandler('news', generate_news))  

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()

    # Schedule the news update task to run every day at a specific time
    updater.job_queue.run_daily(send_news_update, time=time(hour=8, minute=0, tzinfo=pytz.timezone('Europe/Moscow')))

    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == '__main__':
    main()
