import os
from dataclasses import dataclass
from src.constants import ARTIFACT_DIR, DATA_INGESTION_DIR, TRAIN_FILE_NAME, TEST_FILE_NAME

# Artifact Purpose :What output is produced
# It stores configuration for the Data Ingestion component.
# It only defines:Where artifacts go,What paths to use,Folder structure
@dataclass
class DataIngestionConfig:
    artifact_dir: str = ARTIFACT_DIR
    ingestion_dir: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR)
    train_file_path: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR, TRAIN_FILE_NAME)
    test_file_path: str = os.path.join(ARTIFACT_DIR, DATA_INGESTION_DIR, TEST_FILE_NAME)


@dataclass
class DataValidationConfig:
    schema_file_path: str = os.path.join("config", "schema.yaml")
    validation_report_file_path: str = os.path.join("artifacts", "data_validation", "report.yaml")
    
    

@dataclass
class DataTransformationConfig:
    transformed_train_file_path: str = os.path.join("artifacts", "data_transformation", "train.npy")
    transformed_test_file_path: str = os.path.join("artifacts", "data_transformation", "test.npy")
    preprocessor_object_file_path: str = os.path.join("artifacts", "data_transformation", "preprocessor.pkl")

@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model_trainer", "autoencoder_model.h5")