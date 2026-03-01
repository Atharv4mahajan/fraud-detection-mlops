import os
import sys
import numpy as np
import pandas as pd
import pickle
from sklearn.preprocessing import StandardScaler
from src.entity.config_entity import DataTransformationConfig
from src.entity.artifact_entity import DataTransformationArtifact
from src.exception.exception import CustomException
from src.logging.logger import logger


class DataTransformation:

    def __init__(self, config: DataTransformationConfig,
                 train_file_path: str,
                 test_file_path: str):
        self.config = config
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path

    def initiate_data_transformation(self) -> DataTransformationArtifact:
        try:
            logger.info("Starting Data Transformation")

            train_df = pd.read_csv(self.train_file_path)
            test_df = pd.read_csv(self.test_file_path)

            # Separate target
            X_train = train_df.drop("Class", axis=1)
            y_train = train_df["Class"]

            X_test = test_df.drop("Class", axis=1)
            y_test = test_df["Class"]

            # Train only on non-fraud
            X_train_normal = X_train[y_train == 0]

            scaler = StandardScaler()
            scaler.fit(X_train_normal)

            X_train_scaled = scaler.transform(X_train)
            X_test_scaled = scaler.transform(X_test)

            os.makedirs(os.path.dirname(self.config.transformed_train_file_path), exist_ok=True)

            np.save(self.config.transformed_train_file_path, X_train_scaled)
            np.save(self.config.transformed_test_file_path, X_test_scaled)

            with open(self.config.preprocessor_object_file_path, "wb") as f:
                pickle.dump(scaler, f)

            logger.info("Data Transformation Completed")

            return DataTransformationArtifact(
                transformed_train_file_path=self.config.transformed_train_file_path,
                transformed_test_file_path=self.config.transformed_test_file_path,
                preprocessor_object_file_path=self.config.preprocessor_object_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)