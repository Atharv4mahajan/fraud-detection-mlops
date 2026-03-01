import pandas as pd
import sys
from src.configuration.mongo_db_connection import MongoDBClient
from src.exception.exception import CustomException
from src.logging.logger import logger
from src.constants import DATABASE_NAME, COLLECTION_NAME


class FraudData:

    def __init__(self):
        try:
            self.mongo_client = MongoDBClient()
            self.database = self.mongo_client.get_database(DATABASE_NAME)
            self.collection = self.database[COLLECTION_NAME]
        except Exception as e:
            raise CustomException(e, sys)

    def get_data_as_dataframe(self):
        try:
            data = list(self.collection.find())
            df = pd.DataFrame(data)

            if "_id" in df.columns:
                df.drop(columns=["_id"], inplace=True)

            logger.info("Data loaded from MongoDB successfully")
            return df

        except Exception as e:
            raise CustomException(e, sys)