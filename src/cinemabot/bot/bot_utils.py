import inspect
import json
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
    def make_find_reply(info_dict: dict[str, str | None]) -> str:
        info_text = FindCommandUtils.clean_text(info_dict["info"])
        info_text = FindCommandUtils.replace_if_film_is_absent(info_text) + "\n\n"

        year_text = "" if not info_dict["year"] else f" ({info_dict['year'].strip()})"
        poster_text = "" if not info_dict["poster"] else \
            hlink("Посмотреть постер", f"https://ru.wikipedia.org{info_dict['poster']}") + "\n\n"
        rate_text = "" if not info_dict['rate'] else f"Рейтинг: {info_dict['rate'].strip()}/10" + "\n"

        genre_list = [FindCommandUtils.clean_text(g) for g in json.loads(info_dict["genre"])]
        genre_text = ""
        if genre_list:
            genre_text = "Жанр" + ("ы: " if len(genre_list) > 1 else ": ")
            genre_text += ", ".join(genre_list) + "\n"

        links_dict: dict[str, str] = json.loads(info_dict["links"])
        links_text = hbold("К сожалению, ни в одном онлайн-кинотеатре нет этого фильма.")
        if links_dict:
            links_text = hbold("Ссылки на онлайн-кинотеатры \n")
            for service, link in links_dict.items():
                links_text += f"{service}: {hlink('перейти', link)}" + "\n"

        result = hbold(info_dict["title"].strip() + year_text) + "\n" + \
                 f"{genre_text}" + \
                 f"{rate_text}" + \
                 f"{poster_text}" + \
                 f"{info_text}" + \
                 f"{links_text}"

        return result

    @staticmethod
    def clean_text(text: str):
        text = text.replace(u'\xa0', u' ')
        text, _ = re.subn(r"\[\d+]", "", text.strip())
        return text

    @staticmethod
    def replace_if_film_is_absent(text: str):
        if text == "В Википедии нет статьи с таким названием.":
            return "В русскоязычной Википедии нет статьи с таким названием. " \
                   "Вероятно вы неправильно ввели название."

        return text


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
