from telegram import Update
from telegram.ext import ContextTypes
import logging



async def back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents BACK handler
    """
    try:
        from .welcome_handler import welcome
        print("BACK handler is triggered")
        return await welcome(update, context)
    except Exception as error:
        print(f"Error in BACK handler - {error}")
