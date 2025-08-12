from telegram import Update
from telegram.ext import ContextTypes
import logging

from utils.states import ASK_EXPECTATIONS


async def collect_niche(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents NICHE handler
    """
    try:
        logging.info("NICHE handler is triggered")
        client_niche = update.message.text
        context.user_data["client_niche"] = client_niche
        await update.message.reply_text(
            "Занотувала✍🏻! \nОпиши свої очікування від співпраці, якшо такі є:")
        return ASK_EXPECTATIONS
    except Exception as error:
        logging.error(f"Error in EMAIL handler - {error}")
