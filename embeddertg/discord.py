
from telegram import Update
from telegram.ext import ContextTypes

async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Discord Media"""
    if update.message is None:
        return
    if update.message.text is None:
        return
    if (update.message.text.endswith(".mov")):
        print("mymom")
    await context.bot.send_document(
        chat_id=update.message.chat_id,
        document=update.message.text,
        caption=f"Sent by: {update.message.from_user.full_name if update.message.from_user else 'No Name'}")
    await update.message.delete()
