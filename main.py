import os
import logging
import telegram
import asyncio

from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

from utils.convert import convert_to_image
from utils.model import get_image

load_dotenv()

# enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

TELEGRAM_TOKEN: Final = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME: Final = '@PotaaatoBot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(
        chat_id = update.message.chat_id,
        text = 'Hello, I am a potato'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a potato, please type something so i can respond')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')


# Responses

def handle_response(text: str, update: Update) -> str:
    proccessed_text = text.lower()

    file_name = get_image(proccessed_text)
    image = convert_to_image(file_name)

    return image

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type # Checks if its a group or a private chat
    text = update.message.text # the incoming message

    print(f'User ({update.message.chat.id}) in {message_type} chat said: {text}') 

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text, update) 
        else:
            return
    else: 
        response = handle_response(text, update)
    
    await update.message.reply_photo(photo=open(response,'rb'))

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')

def main():
    print('Starting bot... ')
    app =  Application.builder().token(TELEGRAM_TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('custom', custom_command))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    # Error
    app.add_error_handler(error)

    print('Polling...')
    app.run_polling(poll_interval=3)

if __name__ == '__main__':
    main()