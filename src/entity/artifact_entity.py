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