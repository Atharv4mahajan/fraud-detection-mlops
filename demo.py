from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import ModelTrainerConfig

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


transformation_config = DataTransformationConfig()

data_transformation = DataTransformation(
    transformation_config,
    ingestion_artifact.train_file_path,
    ingestion_artifact.test_file_path
)

transformation_artifact = data_transformation.initiate_data_transformation()

print(transformation_artifact)
print("data_transformation successful")



trainer_config = ModelTrainerConfig()

model_trainer = ModelTrainer(
    trainer_config,
    transformation_artifact.transformed_train_file_path
)

trainer_artifact = model_trainer.initiate_model_trainer()

print(trainer_artifact)
print("model_training successful")
