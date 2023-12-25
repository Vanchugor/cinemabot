import dataclasses

from aiohttp import ClientSession

from cinemabot.scraper.scraper_utils import ScraperUtils


@dataclasses.dataclass
class FilmInfo:
    title: str
    genre: str
    year: str
    links: str
    info: str
    rate: str
    poster: str

    @property
    def data(self) -> list[str]:
        return [self.title, self.genre, self.year, self.links, self.info, self.rate, self.poster]


class FilmScraper:
    def __init__(self, session: ClientSession) -> None:
        self.session = session

    def get_wiki_name(self, film_title) -> dict[str, str]:
        query = ScraperUtils.make_google_query(film_title, suffix=" фильм википедия")
        async with self.session.get(query) as response:
            pass

    def lookup(self, film_title: str) -> FilmInfo:
        pass
