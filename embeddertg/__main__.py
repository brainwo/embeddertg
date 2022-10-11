from io import BufferedReader
import os
from telegram import InlineKeyboardMarkup, Message, Update
from telegram._inline.inlinekeyboardbutton import InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters
from yt_dlp import YoutubeDL

YDL_OPTS = {
    'outtmpl': 'output',
    # Sets video to maximum 480p to saves bandwidth
    'format': 'bv[height<=480]+ba/b[height<=480]',
    'overwrites': True
}


# TODO: audio doesn't work somehow
async def twitter(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


async def youtube(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """YouTube videos"""
    with YoutubeDL(YDL_OPTS) as ydl:
        downloading: Message = await context.bot.send_message(
            chat_id=update.message.chat_id,
            text="Downloading video...")
        try:
            download_status = ydl.download(update.message.text)
            if download_status == 0:
                await downloading.edit_text('Sending video...')
                output: BufferedReader = open('output.webm', 'rb')
                await update.message.delete()
                await context.bot.send_video(
                    chat_id=update.message.chat_id,
                    video=output,
                    write_timeout=None,
                    caption=f"Video requested by: {update.message.from_user.full_name}",
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton(text="YouTube Link", url=update.message.text)]])
                )
                await context.bot.delete_message(downloading.chat_id, downloading.message_id)
        except:
            await context.bot.delete_message(downloading.chat_id, downloading.message_id)
            await context.bot.send_message(chat_id=update.message.chat_id, text="Unable to download video")


async def discord(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Discord Media"""
    await context.bot.send_document(
        chat_id=update.message.chat_id,
        document=update.message.text,
        caption=f"Sent by: {update.message.from_user.full_name}")
    await update.message.delete()


def main() -> None:
    token: str = os.environ['BOT_TOKEN']

    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(filters.Regex('twitter.com'), twitter))
    # TODO: need some testing on url regex, preventing reading non-video url
    app.add_handler(MessageHandler(
        filters.Regex('youtube.com') &
        ~filters.Regex('list'), youtube))
    app.add_handler(MessageHandler(
        filters.Regex('discordapp.net'), discord))

    app.run_polling()


if __name__ == "__main__":
    main()
