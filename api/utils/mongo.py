import logging
import os
import urllib.parse

from dotenv import load_dotenv
from pymongo import MongoClient

from api.utils.utils import censor_string


logger = logging.getLogger(__name__)

load_dotenv()

host = os.environ.get("MONGODB_HOST")
port = os.environ.get("MONGODB_PORT")
username = os.environ.get("MONGODB_USERNAME")
password = os.environ.get("MONGODB_PASSWORD")
db_name = os.environ.get("MONGODB_DATABASE")

mongodb_url = f"mongodb://{username}:{urllib.parse.quote(password)}@{host}:{port}"
logger.info(f"URL used for MongoDB connection: mongodb://{username}:{censor_string(urllib.parse.quote(password))}@{host}:{port}")
mongo_motor = MongoClient(mongodb_url)

database = mongo_motor[db_name]
