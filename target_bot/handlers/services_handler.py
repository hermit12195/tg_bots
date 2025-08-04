from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import logging

from database.db import client_check
from utils.states import SERVICES, ASK_NAME, ASK_SOCIAL_NETWORK


async def services(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents SERVICES handler
    """
    try:
        print("SERVICES handler is triggered")
        keyboard = [
            [InlineKeyboardButton("Реклама під ключ", callback_data="ads")],
            [InlineKeyboardButton("Консультація", callback_data="consultation")],
            [InlineKeyboardButton("Аудит реклами", callback_data="audit")],
            [InlineKeyboardButton("Навчання", callback_data="education")],
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.callback_query.message.reply_text("Наразі доступні наступні послуги:", reply_markup=markup)
        return SERVICES
    except Exception as error:
        print(f"Error in SERVICES handler - {error}")


async def service_options(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("SERVICE OPTION in SERVICES handler is triggered")

        query = update.callback_query
        option = query.data
        client_id=update.effective_user.id
        context.user_data["service_type"]=option
        context.user_data["client_id"] = client_id
        client_details = await client_check(client_id)
        if client_details:
            print(client_details)
            context.user_data["signed_up"] = "yes"
            context.user_data["client_id"] = client_details[0]
            context.user_data["client_name"] = client_details[1]
            await context.bot.send_message(chat_id=query.message.chat.id,
                                           text=f"Вітаю, {context.user_data['client_name']}😊!"
                                                "\nНадішли, будь ласка, посилання на твій аккаунт в соцмережі:")
            return ASK_SOCIAL_NETWORK
        else:
            await context.bot.send_message(chat_id=query.message.chat.id, text="Упс😦, здається ми ще не знайомі. Але не хвилюйся це займе одну мить😉 "
                                                                               "\nВкажи, будь ласка, твоє ім'я:")
            return ASK_NAME

    except Exception as error:
        print(f"Error in SERVICE_OPTIONS handler - {error}")