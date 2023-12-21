import asyncio
import logging
import os
import sys

from aiogram import Dispatcher

from cinemabot.bot import CinemaBot
from cinemabot.repository import DBConnector


def main():
    TOKEN = os.getenv("CINEMA_BOT_TOKEN")
    dp = Dispatcher()

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    with DBConnector() as database:
        bot = CinemaBot(dp, database)
        asyncio.run(bot.run(TOKEN))


if __name__ == '__main__':
    main()
