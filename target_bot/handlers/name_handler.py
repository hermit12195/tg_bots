from telegram import Update
from telegram.ext import ContextTypes

from handlers.phone_handler import request_phone
from utils.states import ASK_PHONE
import logging



async def collect_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents NAME handler
    """
    try:
        user_name = update.message.text
        context.user_data["client_name"] = user_name
        print(context.user_data["client_name"])
        print("NAME handler is triggered")
        return await request_phone(update, context)
    except Exception as error:
        print(f"Error in NAME handler - {error}")
