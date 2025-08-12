import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ConversationHandler, \
    CallbackQueryHandler
from handlers import start_handler, welcome_handler, back_handler, name_handler, phone_handler, niche_handler, \
    expectations_handler, social_network_handler
from handlers.services_handler import service_options
from utils.states import HANDLE_OPTION, WELCOME, SERVICES, ASK_NAME, ASK_PHONE, ASK_NICHE, ASK_EXPECTATIONS, \
    ASK_SOCIAL_NETWORK, CONTACTME_OR_MENU, START, SEND_TO_ALL
import logging

logging.basicConfig(
    filename='target_bot.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

load_dotenv()
TOKEN = os.getenv("TOKEN")

app = ApplicationBuilder().token(TOKEN).build()

conv_handler = ConversationHandler(
    entry_points=[CommandHandler("start", start_handler.start)],
    states={
        START: [MessageHandler(filters.TEXT & ~filters.COMMAND, start_handler.start)],
        WELCOME: [MessageHandler(filters.TEXT & ~filters.COMMAND, welcome_handler.welcome)],
        HANDLE_OPTION: [CallbackQueryHandler(welcome_handler.handle_option)],
        SERVICES: [CallbackQueryHandler(service_options), ],
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, name_handler.collect_name)],
        ASK_PHONE: [MessageHandler(filters.CONTACT | (filters.TEXT & ~filters.COMMAND), phone_handler.collect_phone)],
        ASK_NICHE: [MessageHandler(filters.TEXT & ~filters.COMMAND, niche_handler.collect_niche)],
        ASK_EXPECTATIONS: [MessageHandler(filters.TEXT & ~filters.COMMAND, expectations_handler.collect_expectations)],
        ASK_SOCIAL_NETWORK: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, social_network_handler.collect_social_network)],
        CONTACTME_OR_MENU: [CallbackQueryHandler(expectations_handler.handle_option)],
        SEND_TO_ALL: [MessageHandler(filters.TEXT & ~filters.COMMAND, welcome_handler.send_to_all)],
    },
    fallbacks=[CommandHandler("back", back_handler.back)],
    allow_reentry=True,
)
try:
    app.add_handler(conv_handler)
    logging.info("Bot is running...")

    app.run_polling()
except Exception as error:
    logging.error(f"Error during bot initiation in main - {error}")
