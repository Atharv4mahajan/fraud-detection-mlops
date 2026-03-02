from src.components.data_ingestion import DataIngestion
from src.components.data_validation import DataValidation
from src.entity.config_entity import DataIngestionConfig, DataValidationConfig
from src.components.data_transformation import DataTransformation
from src.entity.config_entity import DataTransformationConfig
from src.components.model_trainer import ModelTrainer
from src.entity.config_entity import ModelTrainerConfig
from src.components.model_evaluation import ModelEvaluation
from src.entity.config_entity import ModelEvaluationConfig
from src.components.model_pusher import ModelPusher
from src.entity.config_entity import ModelPusherConfig


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



evaluation_config = ModelEvaluationConfig()

model_evaluation = ModelEvaluation(
    evaluation_config,
    trainer_artifact.trained_model_file_path,
    transformation_artifact.transformed_train_file_path,
    transformation_artifact.transformed_test_file_path,
    ingestion_artifact.test_file_path
)

evaluation_artifact = model_evaluation.initiate_model_evaluation()

print(evaluation_artifact)
print("Evaluation successful")

pusher_config = ModelPusherConfig()

model_pusher = ModelPusher(
    pusher_config,
    trainer_artifact.trained_model_file_path,
    evaluation_artifact.report_file_path
)

pusher_artifact = model_pusher.initiate_model_pusher()

print(pusher_artifact)
