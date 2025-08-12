from telegram import Update
from telegram.ext import ContextTypes

from handlers.phone_handler import request_phone
import logging


async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents NAME handler
    """
    try:
        logging.info("NAME handler is triggered")
        user_name = update.message.text
        context.user_data["client_name"] = user_name
        return await request_phone(update, context)
    except Exception as error:
        logging.error(f"Error in NAME handler - {error}")
