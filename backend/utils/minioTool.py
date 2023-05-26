import os
from datetime import timedelta
from distutils.util import strtobool
from minio import Minio


class MinioClient:
    def __init__(self):
        MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "")
        MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "")
        MINIO_URL = os.environ.get("MINIO_URL", "")
        MINIO_SECURE = bool(strtobool(os.environ.get("MINIO_SECURE", "")))

        self.client = Minio(
            MINIO_URL,
            access_key=MINIO_ACCESS_KEY,
            secret_key=MINIO_SECRET_KEY,
            secure=MINIO_SECURE,
        )

    def upload_file(self, bucket, file_name, file_path):
        found = self.client.bucket_exists(bucket)
        if not found:
            self.client.make_bucket(bucket)

        self.client.fput_object(
            bucket,
            file_name,
            file_path,
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
        return [obj.object_name for obj in objects]

    def bucket_exist(self, bucket):
        return self.client.bucket_exists(bucket)

    def file_in_bucket(self, bucket, filename):
        if filename in self.inspect(bucket):
            return True
        else:
            return False

    def share_url(self, bucket, file_name):
        url = self.client.get_presigned_url(
            "GET", bucket, file_name, expires=timedelta(days=7)
        )
        # url = url.replace('http://172.17.0.1:9000/', '/minio/')
        return url

    def delete_file(self, bucket, file_name):
        try:
            self.client.remove_object(bucket, file_name)
            return "Object removed successfully."
        except:
            return "Failed to remove object."

    def remove_bucket(self, bucket):
        try:
            self.client.remove_bucket(bucket)
            return "Bucket removed successfully."
        except:
            return "Failed to remove bucket."
