from dataclasses import dataclass


# It defines the output produced by a component.

@dataclass
class DataIngestionArtifact:
    train_file_path: str
    test_file_path: str
@dataclass
class DataValidationArtifact:
    validation_status: bool
    report_file_path: str
@dataclass
class DataTransformationArtifact:
    transformed_train_file_path: str
    transformed_test_file_path: str
    preprocessor_object_file_path: str
@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str
@dataclass
class ModelEvaluationArtifact:
    precision: float
    recall: float
    f1_score: float
    roc_auc: float
    threshold: float
    report_file_path: str