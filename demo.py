from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig

# Data Ingestion
ingestion_config = DataIngestionConfig()
data_ingestion = DataIngestion(ingestion_config)
ingestion_artifact = data_ingestion.initiate_data_ingestion()
print("Ingestion successful")
# Data Validation

validation_config = DataValidationConfig()

data_validation = DataValidation(
    validation_config,
    ingestion_artifact.train_file_path,
    ingestion_artifact.test_file_path
)

validation_artifact = data_validation.initiate_data_validation()

print(validation_artifact)
print("validation sucessful")