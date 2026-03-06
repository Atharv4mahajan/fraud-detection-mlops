import os
import sys
import shutil
import yaml

from src.entity.config_entity import ModelPusherConfig
from src.entity.artifact_entity import ModelPusherArtifact
from src.exception.exception import CustomException
from src.logging.logger import logger
from src.configuration.aws_connection import S3Client
from src.constants import MODEL_BUCKET_NAME


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

            artifacts_dir = "artifacts"

            # get latest run folder
            runs = sorted([
                d for d in os.listdir(artifacts_dir)
                if os.path.isdir(os.path.join(artifacts_dir, d)) and d[0].isdigit()
            ])

            if not runs:
                raise Exception("No experiment runs found")

            latest_run = runs[-1]

            # paths
            production_model_path = os.path.join(
                self.config.production_model_dir,
                "model.h5"
            )

            production_report_path = os.path.join(
                self.config.production_model_dir,
                "evaluation_report.yaml"
            )

            production_preprocessor_path = os.path.join(
                self.config.production_model_dir,
                "preprocessor.pkl"
            )

            preprocessor_src = os.path.join(
                artifacts_dir,
                latest_run,
                "data_transformation",
                "preprocessor.pkl"
            )

            s3_client = S3Client()

            # --------------------------------------------
            # CASE 1 : No production model exists
            # --------------------------------------------
            if not os.path.exists(production_model_path):

                shutil.copy(self.model_path, production_model_path)
                shutil.copy(self.evaluation_report_path, production_report_path)
                shutil.copy(preprocessor_src, production_preprocessor_path)

                logger.info("No production model found. Promoting first model.")

                # upload all production artifacts to S3
                for file in os.listdir(self.config.production_model_dir):

                    local_path = os.path.join(self.config.production_model_dir, file)
                    s3_key = f"fraud-detection/{file}"

                    s3_client.upload_file(
                        local_path,
                        MODEL_BUCKET_NAME,
                        s3_key
                    )

                return ModelPusherArtifact(
                    is_model_pushed=True,
                    production_model_path=production_model_path
                )

            # --------------------------------------------
            # CASE 2 : Compare with existing production model
            # --------------------------------------------
            with open(production_report_path, "r") as f:
                production_metrics = yaml.safe_load(f)

            with open(self.evaluation_report_path, "r") as f:
                new_metrics = yaml.safe_load(f)

            if new_metrics["f1_score"] > production_metrics["f1_score"]:

                logger.info("New model better. Promoting new model.")

                shutil.copy(self.model_path, production_model_path)
                shutil.copy(self.evaluation_report_path, production_report_path)
                shutil.copy(preprocessor_src, production_preprocessor_path)

                # upload all artifacts
                for file in os.listdir(self.config.production_model_dir):

                    local_path = os.path.join(self.config.production_model_dir, file)
                    s3_key = f"fraud-detection/{file}"

                    s3_client.upload_file(
                        local_path,
                        MODEL_BUCKET_NAME,
                        s3_key
                    )

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