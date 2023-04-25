import os
from minio import Minio
from datetime import timedelta
from distutils.util import strtobool


class MinioClient:
    def __init__(self):
        MINIO_USER = os.environ.get("MINIO_USER", "minioadmin")
        MINIO_PASSWORD = os.environ.get("MINIO_PASSWORD", "minioadmin")
        MINIO_HOST = os.environ.get("MINIO_HOST", "172.17.0.1")
        MINIO_PORT = os.environ.get("MINIO_PORT", "9000")
        MINIO_SECURE = bool(strtobool(os.environ.get('IE_MINIO_SECURE', "False")))

        minio_username = MINIO_USER
        minio_password = MINIO_PASSWORD
        minio_hostname = MINIO_HOST
        minio_port = MINIO_PORT
        self.client = Minio(
            f"{minio_hostname}:{minio_port}",
            access_key=minio_username,
            secret_key=minio_password,
            secure=MINIO_SECURE,
        )

    def upload_file(self, bucket, file_name, file_path):
        found = self.client.bucket_exists(bucket)
        if not found:
            self.client.make_bucket(bucket)

        self.client.fput_object(
            bucket, file_name, file_path,
        )
    
    def download_file(self, bucket, file_name):
        if not self.client.bucket_exists(bucket):
            return None
        try:
            os.makedirs(f"./image/{bucket}")
        except FileExistsError:
            pass
        file_names = self.inspect(bucket)
        if file_name in file_names:
            output_path = f"./image/{bucket}/{file_name}"
            self.client.fget_object(bucket, file_name, output_path)
            print(f"Finish downloading {output_path}")

    def download_all(self, bucket):
        file_names = self.inspect(bucket)
        for file_name in file_names:
            output_path = f"./image/{bucket}/{file_name}"
            self.client.fget_object(bucket, file_name, output_path)
            print(f"Finish downloading {output_path}")

    def inspect(self, bucket):
        objects = self.client.list_objects(bucket)
        return [obj.object_name.encode('utf-8') for obj in objects]

    def share_url(self, bucket, file_name):
        url = self.client.get_presigned_url(
            "GET",
            bucket,
            file_name,
            expires=timedelta(days=7)
        )
        url = url.replace('http://172.17.0.1:9000/', '/minio/')
        return url

    def delete_file(self, bucket, file_name):
        self.client.remove_object(bucket, file_name)
        print(f"Finish deleting {bucket}/{file_name}")
