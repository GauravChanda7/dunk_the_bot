import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ContextTypes
from exceptions import PinError, UnpinError, BotMessageDeleteError

load_dotenv()

async def pin_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job

    if job is None: return

    chat_id = job.chat_id
    message_id = job.data

    try:
        await context.bot.pin_chat_message(chat_id=chat_id, message_id=message_id)
        print(f"Successfully pinned {message_id} in chat {chat_id}")
    except Exception as e:
        raise PinError(f"Could not pin message {job.data}: {e}") from e


async def unpin_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job

    if job is None: return

    chat_id = job.chat_id
    message_id = job.data

    try:
        await context.bot.unpin_chat_message(chat_id=chat_id, message_id=message_id)
        print(f"Successfully unpinned {message_id} in chat {chat_id}")
    except Exception as e:
        raise UnpinError(f"Could not unpin message {job.data}: {e}") from e

    
async def delete_bot_message(context: ContextTypes.DEFAULT_TYPE):
    job = context.job

    if job is None: return

    chat_id = job.chat_id
    message_id = job.data

    try:
        await context.bot.delete_message(chat_id=chat_id, message_id=message_id)
        print(f"Successfully deleted {message_id} in chat {chat_id}")
    except Exception as e:
        raise BotMessageDeleteError(f"Could not delete message {job.data}: {e}") from e



async def schedule_pin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    if not context.args or len(context.args) < 1:
        await update.message.reply_text("⚠️ Usage: /everyone <message>")
        return
    

    time_seconds = 24*60*60
    text_to_pin = " ".join(context.args)
    mentions = os.getenv("MENTION_LIST")

    sent_message = await context.bot.send_message(
        chat_id=chat_id,
        text = (f"{mentions} \n{text_to_pin}")
    )

    context.job_queue.run_once(
        pin_message,
        0,
        chat_id=chat_id,
        data=sent_message.message_id
    )

    context.job_queue.run_once(
        unpin_message,
        time_seconds,
        chat_id=chat_id,
        data=sent_message.message_id
    )

    context.job_queue.run_once(
        delete_bot_message,
        time_seconds+120,
        chat_id=chat_id,
        data=sent_message.message_id
    )


