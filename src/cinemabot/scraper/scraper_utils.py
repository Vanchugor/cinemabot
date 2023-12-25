import re


class ScraperUtils:
    GOOGLE_SEARCH_BASE = 'https://www.google.com/search?q='
    JUSTWATCH_SEARCH_BASE = 'https://www.justwatch.com/ru/%D0%BF%D0%BE%D0%B8%D1%81%D0%BA?q='

    @staticmethod
    def make_query(search_base: str, sep: str, title: str, suffix: str | None = None) -> str:
        query = title + ("" if suffix is None else suffix)
        normalized_query = ScraperUtils.normalize(query, sep)
        return search_base + normalized_query

    @staticmethod
    def make_justwatch_query(title: str, suffix: str | None = None) -> str:
        return ScraperUtils.make_query(ScraperUtils.JUSTWATCH_SEARCH_BASE, " ", title, suffix)

    @staticmethod
    def make_google_query(title: str, suffix: str | None = None) -> str:
        return ScraperUtils.make_query(ScraperUtils.GOOGLE_SEARCH_BASE, "+", title, suffix)

    @staticmethod
    def normalize(string: str, sep: str) -> str:
        result, _ = re.subn(r"\s+", sep, string.lower())
        return result

    @staticmethod
    def make_wiki_query(wiki_title):
        return f"https://ru.wikipedia.org/wiki/{wiki_title}"
