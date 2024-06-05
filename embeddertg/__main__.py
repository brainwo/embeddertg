#!/usr/bin/env python

import os

from telegram import Update
from telegram.ext import Application, ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters

from discord import handler as discordhandler
from twitter import handler as twitterhandler
from youtube import handler as youtubehandler


async def source(update: Update, _: ContextTypes.DEFAULT_TYPE) -> None:
    """GitHub repository"""
    if update.message is None:
        return
    await update.message.reply_text('This bot is open source and released under MIT license.\nSource code: https://github.com/brainwo/embeddertg')


def main() -> None:
    token: str = os.environ['BOT_TOKEN']

    app: Application = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(
        filters.Regex('discordapp.net') | filters.Regex('cdn.discordapp.com'), discordhandler))
    app.add_handler(MessageHandler(
        filters.Regex('twitter.com'), twitterhandler))
    # TODO: need some testing on url regex, preventing reading non-video url
    app.add_handler(MessageHandler(
        (filters.Regex('youtube.com/watch?') |
         filters.Regex('youtu.be')) &
        ~filters.Regex('list'), youtubehandler))

    app.add_handler(CommandHandler('source', source))

    app.run_polling()


if __name__ == "__main__":
    main()
