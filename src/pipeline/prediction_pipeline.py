import os
import sys
import numpy as np
import pandas as pd
import tensorflow as tf
import pickle
import yaml

from src.exception.exception import CustomException


class PredictionPipeline:

    def __init__(self):
        try:
            artifacts_dir = "artifacts"

            # Filter only timestamp folders (start with digit)
            runs = sorted([
                d for d in os.listdir(artifacts_dir)
                if os.path.isdir(os.path.join(artifacts_dir, d))
                and d[0].isdigit()
            ])

            if not runs:
                raise Exception("No experiment runs found.")

            latest_run = runs[-1]

            self.model_path = os.path.join(
                artifacts_dir,
                "production_model",
                "model.h5"
            )

            self.preprocessor_path = os.path.join(
                artifacts_dir,
                latest_run,
                "data_transformation",
                "preprocessor.pkl"
            )

            if not os.path.exists(self.preprocessor_path):
                raise Exception("Preprocessor not found in latest run.")

            self.model = tf.keras.models.load_model(self.model_path, compile=False)

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

            report_path = os.path.join(
                "artifacts",
                "production_model",
                "evaluation_report.yaml"
            )

            with open(report_path, "r") as f:
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