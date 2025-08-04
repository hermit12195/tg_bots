import json
import os

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackContext
from telegram import InputMediaPhoto
import logging

script_dir = os.path.dirname(os.path.abspath(__file__))
file_path = os.path.join(script_dir, 'cases.json')

async def show_cases(update: Update, context: CallbackContext):
    print("tut")
    with open(file_path, "r", encoding="utf-8") as f:
        cases = json.load(f)

    for case in cases:
        media=[]
        for image_path in case["images"]:
            print(os.path.join(script_dir,image_path))
            media.append(InputMediaPhoto(open(os.path.join(script_dir,image_path), "rb")))
        await context.bot.send_media_group(chat_id=update.effective_chat.id, media=media)

        text = f"💼 *{case['title']}* \n{case['description']}"
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)


