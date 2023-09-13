import os

from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN: Final = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME: Final = '@PotaaatoBot'

# Commands
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Hello, I am a potato')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('I am a potato, please type something so i can respond')

async def custom_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('This is a custom command')


# Responses

def handle_response(text: str) -> str:
    proccessed_text = text.lower()

    if 'hello' in proccessed_text:
        return 'Hello, I am a potato'

    if 'potato' in proccessed_text:
        return 'That is me, I am a potato'
    
    if 'bye' in proccessed_text:
        return 'Bye, I am a potato'
    
    return 'Potato is confused'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type = update.message.chat.type # Checks if its a group or a private chat
    text = update.message.text # the incoming message

    print(f'User ({update.message.chat.id}) in {message_type} chat said: {text}') 

    if message_type == 'group':
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, '').strip()
            response = handle_response(new_text) 
        else:
            return
    else: 
        response = handle_response(text)

    print(f'Bot responded with: {response}')
    await update.message.reply_text(response)

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