from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, \
    ReplyKeyboardRemove
from telegram.ext import ContextTypes

from database.db import create_client, subscribe_client
from handlers.social_network_handler import collect_social_network
from utils.states import ASK_NICHE, ASK_SOCIAL_NETWORK, ASK_PHONE, CONTACTME_OR_MENU
from handlers.welcome_handler import welcome
import logging


async def request_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents PHONE handler
    """
    try:
        phone_button = KeyboardButton("📱Поділись номером телефону", request_contact=True)
        keyboard = [[phone_button]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            f"Дякую, {context.user_data['client_name']}😊! Тепер чекаю на твій номер телефону:",
            reply_markup=markup)
        print("PHONE is triggered")
        return ASK_PHONE
    except Exception as error:
        print(f"Error in PHONE handler - {error}")

async def collect_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.contact is not None:
        client_phone = update.message.contact.phone_number
        context.user_data["client_phone"] = client_phone
        if "service_type" in context.user_data:
            await update.message.reply_text(
                "Занотувала✍🏻! \nНадішли, будь ласка, посилання на твій аккаунт в соцмережі:", reply_markup=ReplyKeyboardRemove())
            return ASK_SOCIAL_NETWORK
        else:
            await update.message.reply_text(
                "Вітаю🤩! Підписка на корисні поради від мене успішно оформлена.")
            await create_client(context.user_data["client_id"], context.user_data["client_name"],context.user_data["client_phone"])
            await subscribe_client(update.effective_user.id)
            keyboard = [
                [InlineKeyboardButton("Написати мені", callback_data="contact_me")],
                [InlineKeyboardButton("Повернутись в головне меню", callback_data="back_to_menu")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            await update.effective_message.reply_text("Вибери опцію:", reply_markup=markup)
            return CONTACTME_OR_MENU
    else:
        phone_button = KeyboardButton("📱Поділись номером телефону", request_contact=True)
        keyboard = [[phone_button]]
        markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
        await update.message.reply_text(
            "Хмммм, здається ти нажав(ла) кнопку 'Поділись номером телефону', давай спробуємо ще раз",
            reply_markup=markup)
        return ASK_PHONE


