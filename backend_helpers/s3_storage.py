import logging
import boto3
from botocore.exceptions import ClientError
from settings import settings


class S3Storage:

    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=settings.ACCESS_KEY_ID,
            aws_secret_access_key=settings.ACCESS_KEY
            )

    def store_data(self, bucket, file_name, object_name):
        if object_name is None:
            object_name = file_name

        try:
            response = self.s3_client.upload_file(file_name, bucket, object_name)
        except ClientError as e:
            logging.error(e)
            return False
        return response

