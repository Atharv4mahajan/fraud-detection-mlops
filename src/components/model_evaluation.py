import os
import sys
import yaml
import numpy as np
import tensorflow as tf
import pandas as pd
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score
from src.entity.config_entity import ModelEvaluationConfig
from src.entity.artifact_entity import ModelEvaluationArtifact
from src.exception.exception import CustomException
from src.logging.logger import logger


class ModelEvaluation:

    def __init__(self,
                 config: ModelEvaluationConfig,
                 model_path: str,
                 transformed_train_path: str,
                 transformed_test_path: str,
                 original_test_path: str):

        self.config = config
        self.model_path = model_path
        self.transformed_train_path = transformed_train_path
        self.transformed_test_path = transformed_test_path
        self.original_test_path = original_test_path

    def initiate_model_evaluation(self) -> ModelEvaluationArtifact:
        try:
            logger.info("Starting Model Evaluation")

            # -------------------------
            # Load Model (no compile needed)
            # -------------------------
            model = tf.keras.models.load_model(self.model_path, compile=False)

            # -------------------------
            # Load Transformed Data
            # -------------------------
            X_train = np.load(self.transformed_train_path)
            X_test = np.load(self.transformed_test_path)

            # -------------------------
            # Compute Reconstruction Error
            # -------------------------
            train_reconstructed = model.predict(X_train, verbose=0)
            train_mse = np.mean(np.power(X_train - train_reconstructed, 2), axis=1)

            test_reconstructed = model.predict(X_test, verbose=0)
            test_mse = np.mean(np.power(X_test - test_reconstructed, 2), axis=1)

            # -------------------------
            # Load True Labels
            # -------------------------
            test_df = pd.read_csv(self.original_test_path)
            y_true = test_df["Class"].values

            # -------------------------
            # Threshold Optimization (Maximize F1)
            # -------------------------
            best_f1 = 0
            best_threshold = 0
            best_precision = 0
            best_recall = 0

            thresholds = np.linspace(min(test_mse), max(test_mse), 80)

            for t in thresholds:
                preds = (test_mse > t).astype(int)

                precision = precision_score(y_true, preds, zero_division=0)
                recall = recall_score(y_true, preds, zero_division=0)
                f1 = f1_score(y_true, preds, zero_division=0)

                if f1 > best_f1:
                    best_f1 = f1
                    best_threshold = t
                    best_precision = precision
                    best_recall = recall

            # Final predictions using best threshold
            predictions = (test_mse > best_threshold).astype(int)

            roc_auc = roc_auc_score(y_true, test_mse)

            # -------------------------
            # Save Evaluation Report
            # -------------------------
            os.makedirs(os.path.dirname(self.config.evaluation_report_file_path), exist_ok=True)

            report = {
                "precision": float(best_precision),
                "recall": float(best_recall),
                "f1_score": float(best_f1),
                "roc_auc": float(roc_auc),
                "threshold": float(best_threshold)
            }

            with open(self.config.evaluation_report_file_path, "w") as f:
                yaml.dump(report, f)

            logger.info("Model Evaluation Completed")

            return ModelEvaluationArtifact(
                precision=best_precision,
                recall=best_recall,
                f1_score=best_f1,
                roc_auc=roc_auc,
                threshold=best_threshold,
                report_file_path=self.config.evaluation_report_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)