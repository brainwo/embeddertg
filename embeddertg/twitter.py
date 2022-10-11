from io import BufferedReader

from telegram import InlineKeyboardMarkup, Message, Update
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.ext import ContextTypes
from yt_dlp import YoutubeDL
from embeddertg import YDL_OPTS


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Twitter videos"""
    with YoutubeDL(YDL_OPTS) as ydl:
        downloading: Message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Downloading video...")
        try:
            download_status = ydl.download(update.message.text)
            if download_status == 0:
                await downloading.edit_text('Sending video...')
                output: BufferedReader = open('output', 'rb')
                await update.message.delete()
                await context.bot.send_video(
                    chat_id=update.message.chat_id,
                    video=output,
                    write_timeout=None,
                    caption=f"Video requested by: {update.message.from_user.full_name}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="Twitter Link", url=update.message.text)]])
                )
                await context.bot.delete_message(downloading.chat_id, downloading.message_id)
        except:
            await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text="Unable to download video")
