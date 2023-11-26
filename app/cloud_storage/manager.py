import boto3
from flask import current_app

class CloudStorageManager:
    def __init__(self):
        self.s3=boto3.client(
                        's3',
                        aws_access_key_id=current_app.config['AWS_ACCESS_KEY'],
                        aws_secret_access_key=current_app.config['AWS_SECRET_KEY'],
                            )
    def store_file(self,file):
        self.s3.upload_fileobj(file, current_app.config['S3_BUCKET_NAME'], file.filename)
        return file.filename

    def load_file(self,file_name):
        save_path='/tmp/'+file_name
        self.s3.download_file(current_app.config['S3_BUCKET_NAME'], file_name, save_path)
        return save_path