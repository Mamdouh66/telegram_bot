import os

from dotenv import load_dotenv
from typing import Final
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

TELEGRAM_TOKEN: Final = os.getenv("TELEGRAM_TOKEN")
BOT_USERNAME: Final = '@PotaaatoBot'