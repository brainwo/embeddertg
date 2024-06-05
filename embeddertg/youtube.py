from io import BufferedReader
import os

from telegram import InlineKeyboardMarkup, Message, Update
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.ext import ContextTypes
from telegram.error import NetworkError
from yt_dlp import YoutubeDL

from __init__ import YDL_OPTS


async def handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """YouTube videos"""
    with YoutubeDL(YDL_OPTS) as ydl:
        if update.message is None:
            return
        downloading: Message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Downloading video...")
        try:
            download_status: int = ydl.download(update.message.text)
            if download_status == 0:
                if os.path.getsize("/tmp/output.mp4") > 50000000:
                    raise Exception("File too large (>50MB)")
                await downloading.edit_text('Sending video...')
                output: BufferedReader = open('/tmp/output.mp4', 'rb')
                #  await update.message.delete()
                await context.bot.send_video(
                    chat_id=update.message.chat_id,
                    video=output,
                    write_timeout=None,
                    caption=f"Video requested by: {
                        update.message.from_user.full_name if update.message.from_user else 'No name'}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="YouTube Link", url=f"{update.message.text}")]])
                )
                await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            else:
                await context.bot.delete_message(downloading.chat_id, downloading.message_id)
                await context.bot.send_message(chat_id=update.message.chat_id, text=f"Unable to download video\nDownload status {download_status}")
        except NetworkError as e:
            print(f"[error] {e}")
            await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"File too large (>50MB)\nDetails: {e}")
        except Exception as e:
            await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text=f"Unable to download video\nDetails: {e}")
