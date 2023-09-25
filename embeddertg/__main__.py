#!/usr/bin/env python

import os

from telegram.ext import Application, ApplicationBuilder, MessageHandler, filters

#  from embeddertg import discord, twitter, youtube
from discord import handler as discordhandler
from twitter import handler as twitterhandler
from youtube import handler as youtubehandler

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

    app.run_polling()


if __name__ == "__main__":
    main()
