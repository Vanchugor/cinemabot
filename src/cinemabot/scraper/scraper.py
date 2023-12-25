import dataclasses
import json
import re

from aiohttp import ClientSession
from bs4 import BeautifulSoup

from cinemabot.definitions import DEFAULT_USER_AGENT
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
    def __init__(self, session: ClientSession, language: str = "RU") -> None:
        self.session = session

    async def get_wiki_title(self, film_title) -> str:
        query = ScraperUtils.make_google_query(film_title, suffix=" фильм википедия")
        headers = {"User-Agent": DEFAULT_USER_AGENT}  # TODO Добавить заголовок языка
        async with self.session.get(query, headers=headers) as response:
            # TODO Просить написать позже при отказе Гугла
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            first_block_tag = soup.find("div", class_="MjjYud")
            header = first_block_tag.find("h3")
            return header.text.removesuffix("- Википедия").strip()

    async def get_data_from_wiki(self, wiki_title: str) -> tuple:
        genre = []
        year = None
        info = None
        poster = None

        query = ScraperUtils.make_wiki_query(wiki_title)
        headers = {"User-Agent": DEFAULT_USER_AGENT}
        async with self.session.get(query, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            main_block = soup.find(id="mw-content-text")
            if main_block:
                info = main_block.find("p").text

                poster_box = main_block.find(class_="infobox-image")
                if poster_box:
                    poster = poster_box.find("a").get("href")

                info_table = main_block.find(class_=re.compile(r"infobox"))
                if info_table:
                    genre_row_header = info_table.find("th", text=re.compile(r"Жанр"))
                    if genre_row_header:
                        genre_info = genre_row_header.find_next("td")
                        genre_info_list = genre_info.findAll("li")
                        if not genre_info_list:
                            genre_info_list = genre_info.findAll("a")

                        if genre_info_list:
                            genre = json.dumps([el.text for el in genre_info_list])

                    year_row_header = info_table.find("th", text=re.compile(r"Год"))
                    if year_row_header:
                        year = year_row_header.find_next("td").text

            return genre, year, info, poster

    async def get_links_and_rate(self, wiki_title: str) -> tuple:
        links = None
        rate = None

        query = ScraperUtils.make_justwatch_query(wiki_title)
        headers = {"User-Agent": DEFAULT_USER_AGENT}
        async with self.session.get(query, headers=headers) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')

            first_film_block = soup.find("div", class_="title-list-row__row")
            if first_film_block:
                picture_wrappers = first_film_block.findAll("picture", class_="picture-wrapper")
                links_dict = dict()
                if picture_wrappers:
                    for pw in picture_wrappers:
                        image = pw.find("img")
                        service = image.get('alt')

                        link_tag = image.find_parent("a")
                        link = link_tag.get('href')
                        links_dict.update([(service, link)])

                links = json.dumps(links_dict)

            rate_block = first_film_block.find("div", class_="jw-scoring-listing__rating")
            if rate_block:
                rate = rate_block.find("span").find("span").text

        return links, rate

    async def lookup(self, film_title: str, normalize: bool = True) -> FilmInfo:
        if normalize:
            wiki_title = await self.get_wiki_title(film_title)
        else:
            wiki_title = film_title

        genre, year, info, poster = await self.get_data_from_wiki(wiki_title)
        links, rate = await self.get_links_and_rate(wiki_title)

        film_info = [
            wiki_title,
            genre,
            year,
            links,
            info,
            rate,
            poster
        ]
        return FilmInfo(*film_info)
