import os
from dataclasses import dataclass
from src.constants import (
    ARTIFACT_DIR,
    DATA_INGESTION_DIR,
    DATA_VALIDATION_DIR,
    DATA_TRANSFORMATION_DIR,
    MODEL_TRAINER_DIR,
    TRAIN_FILE_NAME,
    TEST_FILE_NAME
    
)

@dataclass
class DataIngestionConfig:
    ingestion_dir: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR)
    train_file_path: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR, "train.csv")
    test_file_path: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR, "test.csv")

@dataclass
class DataValidationConfig:
    schema_file_path: str = os.path.join("config", "schema.yaml")
    validation_report_file_path: str = os.path.join(ARTIFACT_DIR, DATA_VALIDATION_DIR, "report.yaml")

@dataclass
class DataTransformationConfig:
    transformed_train_file_path: str = os.path.join(ARTIFACT_DIR, DATA_TRANSFORMATION_DIR, "train.npy")
    transformed_test_file_path: str = os.path.join(ARTIFACT_DIR, DATA_TRANSFORMATION_DIR, "test.npy")
    preprocessor_object_file_path: str = os.path.join(ARTIFACT_DIR, DATA_TRANSFORMATION_DIR, "preprocessor.pkl")

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join(ARTIFACT_DIR, MODEL_TRAINER_DIR, "autoencoder_model.h5")
@dataclass
class ModelEvaluationConfig:
    evaluation_report_file_path: str = os.path.join(
        ARTIFACT_DIR, "model_evaluation", "evaluation_report.yaml"
    )
@dataclass
class ModelPusherConfig:
    production_model_dir: str = os.path.join("artifacts", "production_model")