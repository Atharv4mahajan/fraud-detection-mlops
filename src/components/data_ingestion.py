import os
import sys
from sklearn.model_selection import train_test_split
from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.data_access.fraud_data import FraudData
from src.exception.exception import CustomException
from src.logging.logger import logger


class DataIngestion:

    def __init__(self, config: DataIngestionConfig):
        self.config = config

    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        try:
            logger.info("Starting Data Ingestion")

            fraud_data = FraudData()
            df = fraud_data.get_data_as_dataframe()

            os.makedirs(self.config.ingestion_dir, exist_ok=True)

            train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

            train_df.to_csv(self.config.train_file_path, index=False)
            test_df.to_csv(self.config.test_file_path, index=False)

            logger.info("Data Ingestion Completed")

            return DataIngestionArtifact(
                train_file_path=self.config.train_file_path,
                test_file_path=self.config.test_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)