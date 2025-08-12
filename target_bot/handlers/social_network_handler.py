from telegram import Update
from telegram.ext import ContextTypes
import logging

from utils.states import ASK_NICHE


async def collect_social_network(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents SOCIAL_NETWORK handler
    """
    try:
        logging.info("SOCIAL_NETWORK handler is triggered")
        client_social_network = update.message.text
        context.user_data["client_social_network"] = client_social_network
        await update.message.reply_text(
            "Занотувала✍🏻! \nВкажи нішу в якій тобі потрібні рекламні послуги:")
        return ASK_NICHE
    except Exception as error:
        logging.error(f"Error in SOCIAL_NETWORK handler - {error}")
