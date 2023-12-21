import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
DB_DIR = os.path.join(ROOT_DIR, "../../data")
DEFAULT_DB_FILE = os.path.join(DB_DIR, "cinemabot_db.db")
