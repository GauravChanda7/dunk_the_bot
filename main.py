import logging
import os
from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder, CommandHandler
from telegram.error import InvalidToken
from pin_message import schedule_pin_command
from handlers import error_handler
from exceptions import InvalidBotTokenError
from telegram import BotCommand

load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def post_init(application):
    await application.bot.set_my_commands([
        BotCommand("everyone", "Pin a message and notify everyone")
    ])

if __name__ == '__main__':
    try:
        TOKEN = os.getenv("BOT_TOKEN")

        if not TOKEN:
            raise InvalidBotTokenError("BOT_TOKEN is invalid or missing")
        
        application = ApplicationBuilder().token(TOKEN).post_init(post_init).build()

        application.add_handler(CommandHandler("everyone", schedule_pin_command))
        
        application.add_error_handler(error_handler)
        
        print("🤖 Bot is running...")
        application.run_polling()

    except InvalidBotTokenError as e:
        print(f"❌ CONFIG ERROR: {e}")
        print("💡 Tip: Check your .env file and ensure 'BOT_TOKEN' is set.")
        exit(1)

    except InvalidToken:
        print("❌ TELEGRAM ERROR: The token provided is invalid.")
        print("💡 Tip: Message @BotFather on Telegram to get a new token.")
        exit(1)