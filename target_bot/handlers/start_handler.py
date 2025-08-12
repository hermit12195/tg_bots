from telegram import Update
from telegram.ext import ContextTypes

from database.db import db_conn
from handlers.welcome_handler import welcome
import logging


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents START handler
    """
    try:
        logging.info("START handler is triggered")
        context.user_data.clear()
        context.chat_data.clear()
        await db_conn()
        await update.message.reply_text(
            "Привіт! Я твій помічник з таргетованої реклами. Допоможу обрати послугу, "
            "подивитись приклади робіт або залишити заявку - тисни на потрібний пункт нижче 👇")
        return await welcome(update, context)
    except Exception as error:
        logging.error(f"Error in START handler - {error}")
