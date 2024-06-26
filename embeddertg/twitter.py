from io import BufferedReader

from telegram import InlineKeyboardMarkup, Message, Update
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.ext import ContextTypes
from yt_dlp import YoutubeDL

from __init__ import YDL_OPTS


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Twitter videos"""
    with YoutubeDL(YDL_OPTS) as ydl:
        if update.message is None:
            return
        chat_id = update.message.chat_id
        text = update.message.text
        user = update.message.from_user.full_name if update.message.from_user else "No name"
        downloading: Message = await context.bot.send_message(
            chat_id=chat_id,
            text="Downloading video...")
        try:
            download_status: int = ydl.download(update.message.text)
            if download_status == 0:
                await downloading.edit_text('Sending video...')
                output: BufferedReader = open('output', 'rb')
                await update.message.delete()
                await context.bot.send_video(
                    chat_id=update.message.chat_id,
                    video=output,
                    write_timeout=None,
                    caption=f"Video requested by: {user}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="Twitter Link", url=text)]]) if text is not None else InlineKeyboardMarkup([])
                )
                await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            else:
                await context.bot.delete_message(downloading.chat_id, downloading.message_id)
                await context.bot.send_message(chat_id=update.message.chat_id, text="Unable to download video")
        except Exception as e:
            print(f"[error] {e}")
            await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text="Unable to download video")
