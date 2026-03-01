import os
import sys
import numpy as np
import tensorflow as tf
from tensorflow.keras import layers, models
from src.entity.config_entity import ModelTrainerConfig
from src.entity.artifact_entity import ModelTrainerArtifact
from src.exception.exception import CustomException
from src.logging.logger import logger


class ModelTrainer:

    def __init__(self, config: ModelTrainerConfig, transformed_train_file_path: str):
        self.config = config
        self.train_file_path = transformed_train_file_path

    def build_autoencoder(self, input_dim):

        model = models.Sequential([
            layers.Dense(16, activation="relu", input_shape=(input_dim,)),
            layers.Dense(8, activation="relu"),
            layers.Dense(4, activation="relu"),
            layers.Dense(8, activation="relu"),
            layers.Dense(16, activation="relu"),
            layers.Dense(input_dim, activation="linear")
        ])

        model.compile(optimizer="adam", loss="mse")

        return model

    def initiate_model_trainer(self) -> ModelTrainerArtifact:
        try:
            logger.info("Starting Model Training")

            X_train = np.load(self.train_file_path)

            input_dim = X_train.shape[1]

            model = self.build_autoencoder(input_dim)

            model.fit(
                X_train,
                X_train,
                epochs=10,
                batch_size=256,
                validation_split=0.1,
                verbose=1
            )

            os.makedirs(os.path.dirname(self.config.trained_model_file_path), exist_ok=True)

            model.save(self.config.trained_model_file_path)

            logger.info("Model Training Completed")

            return ModelTrainerArtifact(
                trained_model_file_path=self.config.trained_model_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)