from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler

async def unpin_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job
    chat_id = job.chat_id
    message_id = job.data

    try:
        await context.bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
        print(f"Successfully unpinned {message_id} in chat {chat_id}")
    except Exception as e:
        print(f"Failed to unpin: {e}")
