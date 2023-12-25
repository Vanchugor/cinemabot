import os

# For DB
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, "../../data")
DEFAULT_DB_FILE = os.path.join(DB_DIR, "cinemabot_db.db")

# For bot
TOKEN = os.getenv("CINEMA_BOT_TOKEN")
DEFAULT_USER_AGENT = "Mozilla/5.0 (Windows NT 6.1; rv:84.0) Gecko/20100101 Firefox/84.0"
