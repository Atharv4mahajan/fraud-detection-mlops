import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import yaml

from src.exception.exception import CustomException
from src.configuration.aws_connection import S3Client
from src.constants import MODEL_BUCKET_NAME


class PredictionPipeline:

    def __init__(self):
        try:

            artifacts_dir = "artifacts"
            production_dir = os.path.join(artifacts_dir, "production_model")

            os.makedirs(production_dir, exist_ok=True)

            self.model_path = os.path.join(production_dir, "model.h5")
            self.preprocessor_path = os.path.join(production_dir, "preprocessor.pkl")
            self.report_path = os.path.join(production_dir, "evaluation_report.yaml")

            s3_client = S3Client()

            # download artifacts if missing
            if not os.path.exists(self.model_path):
                s3_client.download_file(
                    MODEL_BUCKET_NAME,
                    "fraud-detection/model.h5",
                    self.model_path
                )

            if not os.path.exists(self.preprocessor_path):
                s3_client.download_file(
                    MODEL_BUCKET_NAME,
                    "fraud-detection/preprocessor.pkl",
                    self.preprocessor_path
                )

            if not os.path.exists(self.report_path):
                s3_client.download_file(
                    MODEL_BUCKET_NAME,
                    "fraud-detection/evaluation_report.yaml",
                    self.report_path
                )

            # load model
            self.model = tf.keras.models.load_model(self.model_path, compile=False)

            # load preprocessor
            with open(self.preprocessor_path, "rb") as f:
                self.preprocessor = pickle.load(f)

        except Exception as e:
            raise CustomException(e, sys)

    def predict(self, input_data: dict):

        try:

            df = pd.DataFrame([input_data])

            transformed = self.preprocessor.transform(df)

            reconstruction = self.model.predict(transformed)

            mse = np.mean(np.power(transformed - reconstruction, 2), axis=1)

            with open(self.report_path, "r") as f:
                report = yaml.safe_load(f)

            threshold = report["threshold"]

            prediction = int(mse[0] > threshold)

            return {
                "fraud_prediction": prediction,
                "reconstruction_error": float(mse[0]),
                "threshold": float(threshold)
            }

        except Exception as e:
            raise CustomException(e, sys)