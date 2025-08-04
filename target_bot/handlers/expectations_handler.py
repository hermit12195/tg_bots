import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

from database.db import create_client, create_order, client_check

import logging

from google_doc.integrator import append_text_to_doc
from handlers.welcome_handler import welcome
from utils.states import CONTACTME_OR_MENU

load_dotenv()
DOCUMENT_ID = os.getenv("DOCUMENT_ID")
ADMIN_ID = os.getenv("ADMIN_ID")

async def collect_expectations(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents PHONE handler
    """
    try:
        client_expectations = update.message.text
        context.user_data["client_expectations"] = client_expectations
        print("EXPECTATIONS handler is triggered")
        return await create(update, context)
    except Exception as error:
        print(f"Error in EXPECTATIONS handler - {error}")


async def create(update, context):
    """
    """
    try:
        if "signed_up" in context.user_data:
            await create_order(context.user_data["client_id"],
                               context.user_data["client_social_network"],
                               context.user_data["client_niche"],
                               context.user_data["client_expectations"],
                               context.user_data["service_type"])
            client_details= await client_check(context.user_data["client_id"])
            client_details= (f"Нове замолення: \n"
                             f"Тип: {context.user_data['service_type']}\n"
                             f"Ім'я: {client_details[1]}\n"
                             f"Номер телефону: {client_details[2]}\n"
                             f"Соцмережа: {context.user_data['client_social_network']}\n"
                             f"Ніша: {context.user_data['client_niche']}\n"
                             f"Очікування: {context.user_data['client_expectations']}\n")
            await update.message.reply_text("⏳ Обробляю запит...")
            append_text_to_doc(DOCUMENT_ID,client_details)
            await context.bot.send_message(chat_id=ADMIN_ID, text=client_details)
        else:
            await create_client(context.user_data["client_id"], context.user_data["client_name"],
                                context.user_data["client_phone"])
            await create_order(context.user_data["client_id"],
                               context.user_data["client_social_network"],
                               context.user_data["client_niche"],
                               context.user_data["client_expectations"],
                               context.user_data["service_type"])
            client_details = (f"Нове замолення: \n"
                              f"Тип: {context.user_data['service_type']}\n"
                              f"Ім'я: {context.user_data['client_name']}\n"
                              f"Номер телефону: {context.user_data['client_phone']}\n"
                              f"Соцмережа: {context.user_data['client_social_network']}\n"
                              f"Ніша: {context.user_data['client_niche']}\n"
                              f"Очікування: {context.user_data['client_expectations']}\n")
            await update.message.reply_text("⏳ Обробляю запит...")
            append_text_to_doc(DOCUMENT_ID, client_details)
            await context.bot.send_message(chat_id=ADMIN_ID, text=client_details)
        await context.bot.send_message(chat_id=context.user_data["client_id"],
                                       text=f"🟢 “Твоя заявка успішно прийнята! Я зв’яжусь із тобою найближчим часом🤓. Якщо потрібно - можеш написати мені тут прямо зараз")
        keyboard = [
            [InlineKeyboardButton("Написати мені", callback_data="contact_me")],
            [InlineKeyboardButton("Повернутись в головне меню", callback_data="back_to_menu")]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.effective_message.reply_text("Вибери опцію:", reply_markup=markup)
        return CONTACTME_OR_MENU
    except Exception as error:
        print(f"Error during user update - {error}")


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        print("HANDLE OPTION in EXPECTATIONS handler is triggered")
        query = update.callback_query
        option = query.data
        if option == "back_to_menu":
            return await welcome(update, context)
        else:
            await context.bot.send_message(chat_id=query.from_user.id,
                                           text="Я відповідаю щодня з 10:00 до 19:00 💬: https://t.me/smar1owl")
    except Exception as error:
        print(f"Error with HANDLE option in EXPECTATIONS handler - {error}")
