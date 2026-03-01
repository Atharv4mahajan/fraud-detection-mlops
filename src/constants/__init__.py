
# from datetime import datetime

# TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

# ARTIFACT_DIR = f"artifacts/{TIMESTAMP}"
DATABASE_NAME = "fraud_database"
COLLECTION_NAME = "fraud_data"


# DATA_INGESTION_DIR = "data_ingestion"
# DATA_VALIDATION_DIR = "data_validation"
# DATA_TRANSFORMATION_DIR = "data_transformation"
# MODEL_TRAINER_DIR = "model_trainer"
# TRAIN_FILE_NAME = "train.csv"
# TEST_FILE_NAME = "test.csv"
from datetime import datetime

TIMESTAMP = datetime.now().strftime("%Y_%m_%d_%H_%M_%S")

ARTIFACT_DIR = f"artifacts/{TIMESTAMP}"

DATA_INGESTION_DIR = "data_ingestion"
DATA_VALIDATION_DIR = "data_validation"
DATA_TRANSFORMATION_DIR = "data_transformation"
MODEL_TRAINER_DIR = "model_trainer"
TRAIN_FILE_NAME = "train.csv"
TEST_FILE_NAME = "test.csv"