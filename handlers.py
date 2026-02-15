# handlers.py
from telegram.ext import ContextTypes
from exceptions import PinError, UnpinError, BotMessageDeleteError

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    """Log the error and handle specific custom exceptions."""
    error = context.error

    if isinstance(error, PinError):
        print(f"⚠️ [PIN ERROR] {error}")
    elif isinstance(error, UnpinError):
        print(f"ℹ️ [UNPIN INFO] {error}")
    elif isinstance(error, BotMessageDeleteError):
        print(f"⚠️ [DELETE ERROR] {error}")
    else:
        print(f"❌ [CRITICAL] {error}")