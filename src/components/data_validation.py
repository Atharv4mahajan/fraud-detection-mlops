import os
import sys
import yaml
import pandas as pd
from scipy.stats import ks_2samp
from src.entity.config_entity import DataValidationConfig
from src.entity.artifact_entity import DataValidationArtifact
from src.exception.exception import CustomException
from src.logging.logger import logger


class DataValidation:

    def __init__(self, config: DataValidationConfig, train_file_path: str, test_file_path: str):
        self.config = config
        self.train_file_path = train_file_path
        self.test_file_path = test_file_path

    def validate_schema(self, df: pd.DataFrame) -> bool:
        with open(self.config.schema_file_path, 'r') as file:
            schema = yaml.safe_load(file)

        expected_columns = schema['columns']

        # Column existence check
        if set(expected_columns.keys()) != set(df.columns):
            logger.error("Column mismatch detected")
            return False

        # Data type validation
        for col, dtype in expected_columns.items():
            if str(df[col].dtype) != dtype:
                logger.error(f"Data type mismatch in column {col}")
                return False

        # Target column check
        if schema['target_column'] not in df.columns:
            logger.error("Target column missing")
            return False

        return True

    def check_missing_values(self, df: pd.DataFrame) -> bool:
        if df.isnull().sum().sum() > 0:
            logger.error("Missing values detected")
            return False
        return True

    def detect_data_drift(self, train_df: pd.DataFrame, test_df: pd.DataFrame) -> bool:
        drift_detected = False

        for col in train_df.columns:
            statistic, p_value = ks_2samp(train_df[col], test_df[col])
            if p_value < 0.05:
                logger.warning(f"Drift detected in column {col}")
                drift_detected = True

        return drift_detected

    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            logger.info("Starting Data Validation")

            train_df = pd.read_csv(self.train_file_path)
            test_df = pd.read_csv(self.test_file_path)

            os.makedirs(os.path.dirname(self.config.validation_report_file_path), exist_ok=True)

            schema_valid = self.validate_schema(train_df)
            missing_valid = self.check_missing_values(train_df)
            drift_detected = self.detect_data_drift(train_df, test_df)

            validation_status = schema_valid and missing_valid and not drift_detected

            report = {
                "schema_valid": schema_valid,
                "missing_values_valid": missing_valid,
                "drift_detected": drift_detected,
                "final_validation_status": validation_status
            }

            with open(self.config.validation_report_file_path, "w") as file:
                yaml.dump(report, file)

            logger.info("Data Validation Completed")

            return DataValidationArtifact(
                validation_status=validation_status,
                report_file_path=self.config.validation_report_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)