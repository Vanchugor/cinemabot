import asyncio
import logging
import os
import sys

from aiogram import Dispatcher
from aiogram.client.session import aiohttp
from aiogram.fsm.strategy import FSMStrategy

from cinemabot.bot import CinemaBot
from cinemabot.repository import DBManager


def main():
    TOKEN = os.getenv("CINEMA_BOT_TOKEN")
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_TOPIC)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    with DBManager() as db_manager:
        async with aiohttp.ClientSession() as session:
            bot = CinemaBot(TOKEN, dp, db_manager, session)
            asyncio.run(bot.run())


if __name__ == '__main__':
    main()
