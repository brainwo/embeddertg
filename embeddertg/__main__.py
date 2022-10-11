#!/usr/bin/env python

import os
from telegram.ext import ApplicationBuilder, MessageHandler, filters

from embeddertg import youtube, twitter, discord


def main() -> None:
    token: str = os.environ['BOT_TOKEN']

    app = ApplicationBuilder().token(token).build()

    app.add_handler(MessageHandler(
        filters.Regex('discordapp.net'), discord.handler))
    app.add_handler(MessageHandler(
        filters.Regex('twitter.com'), twitter.handler))
    # TODO: need some testing on url regex, preventing reading non-video url
    app.add_handler(MessageHandler(
        filters.Regex('youtube.com') &
        ~filters.Regex('list'), youtube.handler))

    app.run_polling()


if __name__ == "__main__":
    main()
