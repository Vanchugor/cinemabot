import re


class ScraperUtils:
    GOOGLE_SEARCH_BASE = 'https://www.google.com/search?q='

    @staticmethod
    def make_google_query(query: str, suffix: str | None) -> str:
        query = query + ("" if suffix is None else suffix)
        normalized_query = ScraperUtils.normalize(query)
        return ScraperUtils.GOOGLE_SEARCH_BASE + normalized_query

    @staticmethod
    def normalize(string: str) -> str:
        result, _ = re.subn(r"\s+", "+", string.lower())
        return result
