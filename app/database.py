from mongoengine import connect
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_DB_NAME = os.getenv("MONGO_DB_NAME")
MONGO_HOST = os.getenv("MONGO_HOST")
MONGO_PORT = int(os.getenv("MONGO_PORT", 27017))

if not MONGO_DB_NAME:
    raise ValueError("MONGO_DB_NAME is not set")

connect(
    db=MONGO_DB_NAME,
    host=MONGO_HOST,
    port=MONGO_PORT
)