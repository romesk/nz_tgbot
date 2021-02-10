import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

ADMIN_ID = os.getenv("ADMIN_ID")

PG_USER = os.getenv("PG_USER")
PG_PASSWORD = os.getenv("PG_PASSWORD")
PG_NAME = os.getenv("PG_NAME")

ip = os.getenv("ip")

POSTGRES_URI = f'postgresql://{PG_USER}:{PG_PASSWORD}@{ip}/{PG_NAME}'


