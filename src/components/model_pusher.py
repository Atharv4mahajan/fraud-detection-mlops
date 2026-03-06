import os
import sys
import shutil
import yaml

from src.entity.config_entity import ModelPusherConfig
from src.entity.artifact_entity import ModelPusherArtifact
from src.exception.exception import CustomException
from src.logging.logger import logger
from src.configuration.aws_connection import S3Client
from src.constants import MODEL_BUCKET_NAME, MODEL_S3_KEY, EVALUATION_S3_KEY


class ModelPusher:

    def __init__(self,
                 config: ModelPusherConfig,
                 model_path: str,
                 evaluation_report_path: str):

        self.config = config
        self.model_path = model_path
        self.evaluation_report_path = evaluation_report_path

    def initiate_model_pusher(self) -> ModelPusherArtifact:
        try:
            logger.info("Starting Model Pusher")

            os.makedirs(self.config.production_model_dir, exist_ok=True)

            production_model_path = os.path.join(
                self.config.production_model_dir,
                "model.h5"
            )

            production_report_path = os.path.join(
                self.config.production_model_dir,
                "evaluation_report.yaml"
            )

            s3_client = S3Client()

            # --------------------------------------------
            # CASE 1: No production model exists
            # --------------------------------------------
            if not os.path.exists(production_model_path):

                shutil.copy(self.model_path, production_model_path)
                shutil.copy(self.evaluation_report_path, production_report_path)

                # Upload model
                s3_client.upload_file(
                    production_model_path,
                    MODEL_BUCKET_NAME,
                    MODEL_S3_KEY
                )

                # Upload evaluation report
                s3_client.upload_file(
                    production_report_path,
                    MODEL_BUCKET_NAME,
                    EVALUATION_S3_KEY
                )

                logger.info("No production model found. Model promoted and uploaded to S3.")

                return ModelPusherArtifact(
                    is_model_pushed=True,
                    production_model_path=production_model_path
                )

            # --------------------------------------------
            # CASE 2: Compare new model with production
            # --------------------------------------------
            with open(production_report_path, "r") as f:
                production_metrics = yaml.safe_load(f)

            with open(self.evaluation_report_path, "r") as f:
                new_metrics = yaml.safe_load(f)

            if new_metrics["f1_score"] > production_metrics["f1_score"]:

                shutil.copy(self.model_path, production_model_path)
                shutil.copy(self.evaluation_report_path, production_report_path)

                # Upload updated model
                s3_client.upload_file(
                    production_model_path,
                    MODEL_BUCKET_NAME,
                    MODEL_S3_KEY
                )

                # Upload updated report
                s3_client.upload_file(
                    production_report_path,
                    MODEL_BUCKET_NAME,
                    EVALUATION_S3_KEY
                )

                logger.info("New model better. Promoted and uploaded to S3.")

                return ModelPusherArtifact(
                    is_model_pushed=True,
                    production_model_path=production_model_path
                )

            else:

                logger.info("New model worse. Not promoted.")

                return ModelPusherArtifact(
                    is_model_pushed=False,
                    production_model_path=production_model_path
                )

        except Exception as e:
            raise CustomException(e, sys)