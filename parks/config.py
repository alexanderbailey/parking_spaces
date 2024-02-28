from dotenv import load_dotenv, find_dotenv
from os import getenv
load_dotenv(find_dotenv())

db_host = getenv("DB_HOST")
db_port = getenv("DB_PORT")
db_name = getenv("DB_NAME")
db_user = getenv("DB_USER")
db_pass = getenv("DB_PASS")
db_url = f"postgresql://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"