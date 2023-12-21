import logging
import sqlite3

from aiogram import Bot, Dispatcher, types, F
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart, Command
from pydantic import ValidationError

from cinemabot.bot.bot_utils import *


# TODO Сделать ChatMemberUpdated функцию для новичков
class CinemaBot:
    def __init__(self, dispatcher: Dispatcher, database: sqlite3.Cursor) -> None:
        self.database: sqlite3.Cursor = database
        self.dp: Dispatcher = dispatcher
        self.help = HelpCommandUtils.make_help_list(self)

        self.dp.message(F.text.regexp(r"^[a-zA-Z0-9а-яА-Я]$"))(self.command_find_handler)
        self.dp.message(Command("find"))(self.command_find_handler)
        self.dp.message(Command("help"))(self.command_help_handler)
        self.dp.message(CommandStart())(self.command_start_handler)

    async def command_find_handler(self, message: types.Message) -> None:
        """
        Looks for links to online cinemas by film title sent. This is the default command,
        meaning you just need to send the movie title. But you can still use /find.

        :RU Ищет ссылки на онлайн-кинотеатры по заданному названию фильма. Это команда по умолчанию,
        то есть достаточно просто послать название фильма. Однако все равно можно использовать /find
        в начале запроса.

        :param message: message received
        :return: None
        """
        if not message.text:
            await message.answer(ErrorUtils.make_type_mismatch_reply("текст"))

        await message.answer(FindCommandUtils.make_find_reply(message))

    async def command_start_handler(self, message: Message) -> None:
        """
        Greets user.
        :RU Приветствует пользователя.

        :param message: message received
        :return: None
        """
        await message.answer(StartCommandUtils.make_start_reply(message))

    async def command_help_handler(self, message: Message) -> None:
        """
        Shows a list of available commands.
        :RU Показывает список доступных команд.

        :param message: message received
        :return: None
        """
        try:
            await message.answer(self.help)
        except ValidationError as e:
            logging.log(level=logging.ERROR, msg=str(e))
            await message.answer(ErrorUtils.DEFAULT_REPLY)

    async def run(self, token: str) -> None:
        bot = Bot(token, parse_mode=ParseMode.HTML)
        await self.dp.start_polling(bot)
