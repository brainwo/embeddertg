
from telegram import Update
from telegram.ext import ContextTypes


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Discord Media"""
    await context.bot.send_document(
        chat_id=update.message.chat_id,
        document=update.message.text,
        caption=f"Sent by: {update.message.from_user.full_name}")
    await update.message.delete()
