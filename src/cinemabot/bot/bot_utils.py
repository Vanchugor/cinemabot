import inspect
import re
import typing as tp

from aiogram.types import Message
from aiogram.utils.markdown import hbold, hlink

from cinemabot.scraper.scraper import FilmInfo


# TODO Сделать протокол

class StartCommandUtils:
    @staticmethod
    def make_start_reply(message: Message) -> str:
        return (f"Привет, {hbold(message.from_user.full_name)}! "
                + f"Как кино-бот, готов предложить тебе свои скромные услуги по поиску кино. "
                + f"Скажи /help, чтобы узнать список доступных команд.")


class FindCommandUtils:
    @staticmethod
    def make_find_reply(info: FilmInfo) -> str:
        return ", ".join(info.data)


class HelpCommandUtils:
    PREFIX = "command_"
    SUFFIX = "_handler"
    DEFAULT_REPLY = "Название говорящее."
    HIDDEN_COMMANDS = {"start"}

    @staticmethod
    def extract_locale_doc(doc: str, locale: str = "RU") -> str:
        description = HelpCommandUtils.DEFAULT_REPLY

        doc_parts = doc.split(":")
        if len(doc_parts) == 0 or len(doc_parts) == 1:
            return description

        for part in doc_parts:
            if part.startswith(locale):
                description = part.removeprefix(locale)
                break

        return re.sub(r"\s+", " ", description.strip())

    @staticmethod
    def make_help_list(bot: tp.Any) -> str:
        message = ""
        methods = inspect.getmembers(bot, predicate=inspect.ismethod)
        for method in methods:
            if method[0].startswith(HelpCommandUtils.PREFIX) and method[0].endswith(HelpCommandUtils.SUFFIX):
                command_name = method[0].removeprefix(HelpCommandUtils.PREFIX).removesuffix(HelpCommandUtils.SUFFIX)
                if command_name in HelpCommandUtils.HIDDEN_COMMANDS:
                    continue

                command_doc = HelpCommandUtils.extract_locale_doc(method[1].__doc__)
                message += "/" + command_name + " - "
                message += command_doc + "\n\n"

        return message.removesuffix("\n\n")


class HistoryCommandUtils:

    @staticmethod
    def make_history_reply(data: list[tuple], limit: int) -> str:
        if not data:
            return "История запросов пуста."

        reply = f"Последние запросы (лимит {limit}):\n"
        number = 1
        for name, year, message_id in data:
            name_year_formated = f"{name}({year})"
            post_command = f"/give_{message_id}"
            reply += f"{number}. {name_year_formated} {post_command}\n"
            number += 1

        return reply


class ErrorUtils:
    DEFAULT_REPLY = "Что-то пошло не так. Попробуй еще раз."

    @staticmethod
    def make_i_expected_reply(right_type: str):
        return f"Я ожидал {right_type.lower()}."
