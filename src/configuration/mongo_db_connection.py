import os
from pymongo import MongoClient
from dotenv import load_dotenv
from src.exception.exception import CustomException
from src.logging.logger import logger
import sys

load_dotenv()

class MongoDBClient:
    client = None

    def __init__(self):
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv("MONGODB_URL")
                MongoDBClient.client = MongoClient(mongo_db_url)
                logger.info("MongoDB connection established")
        except Exception as e:
            raise CustomException(e, sys)

    def get_database(self, database_name: str):
        return MongoDBClient.client[database_name]