import os

from dotenv import load_dotenv
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from database.db import client_check, subscribe_client, client_list
from handlers import cases_handler
from handlers.services_handler import services
from utils.states import HANDLE_OPTION, ASK_NAME, SEND_TO_ALL, CONTACTME_OR_MENU
import logging

load_dotenv()
ADMIN_ID = os.getenv("ADMIN_ID")


async def welcome(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Represents WELCOME handler
    """
    try:
        logging.info("WELCOME handler is triggered")
        keyboard = [
            [InlineKeyboardButton("Послуги", callback_data="services")],
            [InlineKeyboardButton("Мої кейси&відгуки", callback_data="cases")],
            [InlineKeyboardButton("Підписатись на розсилку корисних порад", callback_data="subscription")],
            [InlineKeyboardButton("Написати мені", callback_data="contactme")],
        ]
        if update.effective_user.id == int(ADMIN_ID):
            keyboard.append([InlineKeyboardButton("Відправити всім", callback_data="admin")])
        markup = InlineKeyboardMarkup(keyboard)
        await update.effective_message.reply_text("Вибери опцію:", reply_markup=markup)
        return HANDLE_OPTION
    except Exception as error:
        logging.info(f"Error in WELCOME handler - {error}")


async def handle_option(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """
    Handles callback query options from the main (welcome) menu.

    Supported options:
    - "services": navigates to the services flow.
    - "cases": shows previous case examples and provides contact options.
    - "subscription": checks subscription status and subscribes if needed.
    - "contactme": sends contact info with reply markup.
    - "admin": allows admin to send a broadcast message to all subscribers.

    Args:
        update (telegram.Update): Incoming update from the user.
        context (telegram.ext.CallbackContext): Context containing user data and bot instance.

    Returns:
        int: The next conversation state (e.g. CONTACTME_OR_MENU, ASK_NAME, SEND_TO_ALL), or None.
    """
    try:
        logging.info("HANDLE OPTION in WELCOME handler is triggered")
        query = update.callback_query
        option = query.data
        if option == "services":
            return await services(update, context)
        elif option == "cases":
            await cases_handler.show_cases(update, context)
            keyboard = [
                [InlineKeyboardButton("Написати мені", callback_data="contact_me")],
                [InlineKeyboardButton("Повернутись в головне меню", callback_data="back_to_menu")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text="❕Бажаєте, щоб про вас дізнались🤩, та залучити більше клієнтів, звертайтесь у direct 💌")
            await update.effective_message.reply_text("Вибери опцію:", reply_markup=markup)
            return CONTACTME_OR_MENU
        elif option == "subscription":
            client_details = await client_check(update.effective_user.id)
            if client_details:
                if client_details[3] == "no":
                    await subscribe_client(update.effective_user.id)
                    await context.bot.send_message(chat_id=query.message.chat.id,
                                                   text="Вітаю🤩! Ти успішно підписався(лась) на розсилку корисних порад від мене.")
                    keyboard = [
                        [InlineKeyboardButton("Написати мені", callback_data="contact_me")],
                        [InlineKeyboardButton("Повернутись в головне меню", callback_data="back_to_menu")]
                    ]
                    markup = InlineKeyboardMarkup(keyboard)
                    await update.effective_message.reply_text("Вибери опцію:", reply_markup=markup)
                    return CONTACTME_OR_MENU
                else:
                    await context.bot.send_message(chat_id=query.message.chat.id,
                                                   text="Ти вже підписаний(а) на розсилку корисних порад від мене. Очікуй на поради🤓")
                    keyboard = [
                        [InlineKeyboardButton("Написати мені", callback_data="contact_me")],
                        [InlineKeyboardButton("Повернутись в головне меню", callback_data="back_to_menu")]
                    ]
                    markup = InlineKeyboardMarkup(keyboard)
                    await update.effective_message.reply_text("Вибери опцію:", reply_markup=markup)
                    return CONTACTME_OR_MENU
            else:
                context.user_data["client_id"] = update.effective_user.id
                await context.bot.send_message(chat_id=query.message.chat.id,
                                               text="Упс😦, здається ми ще не знайомі. Але не хвилюйся це займе одну мить😉 "
                                                    "\nВкажи, будь ласка, твоє ім'я:")
                return ASK_NAME
        elif option == "contactme":
            await context.bot.send_message(chat_id=query.from_user.id,
                                           text="Я відповідаю щодня з 10:00 до 19:00 💬: https://t.me/smar1owl")
            keyboard = [
                [InlineKeyboardButton("Головне меню", callback_data="back_to_menu")]
            ]
            markup = InlineKeyboardMarkup(keyboard)
            await update.effective_message.reply_text("👆", reply_markup=markup)
            return CONTACTME_OR_MENU
        elif option == "admin":
            await context.bot.send_message(chat_id=query.message.chat.id,
                                           text="Введи повідомлення, яке буде відправлено всім підписаним на розсилку порад користувачам:")
            return SEND_TO_ALL

    except Exception as error:
        logging.error(f"Error in HANDLE OPTION in WELCOME handler - {error}")


async def send_to_all(update, context):
    """
    Sends a broadcast message to all subscribers
    """
    try:
        logging.info("SEND_TO_ALL function in WELCOME handler is triggered")
        c_list = await client_list()
        for c_id in c_list:
            await context.bot.send_message(chat_id=c_id[0],
                                           text=update.message.text)
    except Exception as error:
        logging.error(f"Error in HANDLE SEND_TO_ALL in WELCOME handler - {error}")
