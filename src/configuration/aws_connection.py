import boto3
from src.exception.exception import CustomException
import sys


class S3Client:

    def __init__(self):
        try:
            # Let boto3 automatically read env variables
            self.s3 = boto3.client("s3")
        except Exception as e:
            raise CustomException(e, sys)

    def upload_file(self, file_path: str, bucket_name: str, s3_key: str):
        try:
            self.s3.upload_file(file_path, bucket_name, s3_key)
        except Exception as e:
            raise CustomException(e, sys)

    def download_file(self, bucket_name: str, s3_key: str, file_path: str):
        try:
            self.s3.download_file(bucket_name, s3_key, file_path)
        except Exception as e:
            raise CustomException(e, sys)