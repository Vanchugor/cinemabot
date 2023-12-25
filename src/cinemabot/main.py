import asyncio
import logging
import os
import sys

from aiogram import Dispatcher
from aiogram.client.session import aiohttp
from aiogram.fsm.strategy import FSMStrategy

from cinemabot.bot import CinemaBot
from cinemabot.definitions import TOKEN
from cinemabot.repository import DBManager


async def main():
    dp = Dispatcher(fsm_strategy=FSMStrategy.USER_IN_TOPIC)

    logging.basicConfig(level=logging.INFO, stream=sys.stdout)

    with DBManager() as db_manager:
        async with aiohttp.ClientSession() as session:
            bot = CinemaBot(TOKEN, dp, db_manager, session)
            await bot.run()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
    loop.close()
