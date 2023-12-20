import asyncio
import logging
import os
import sys

from cinemabot.bot.echo_bot import run_echo_bot


def main():
    TOKEN = os.getenv("CINEMA_BOT_TOKEN")
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(run_echo_bot(TOKEN))


if __name__ == '__main__':
    main()
