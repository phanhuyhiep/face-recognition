import uuid
import io

from urllib.parse import urlparse
from fastapi import UploadFile
from minio.error import S3Error

from configs.index import minio_client
from configs.minio_config import MinioSettings

async def upload_to_minio(file: UploadFile, bucket: str = MinioSettings.MINIO_BUCKET) -> str:
    try:
        found = minio_client.bucket_exists(bucket)
        if not found:
            minio_client.make_bucket(bucket)
        file_extension = file.filename.split(".")[-1]
        object_name = f"{uuid.uuid4().hex}.{file_extension}"
        file_bytes = await file.read()
        file_size = len(file_bytes)
        minio_client.put_object(
            bucket_name=bucket,
            object_name=object_name,
            data=io.BytesIO(file_bytes),
            length=file_size,
            content_type=file.content_type
        )
        url = f"{MinioSettings.MINIO_ENDPOINT}/{bucket}/{object_name}"
        return url
    except S3Error as e:
        raise HTTPException(status_code=500, detail=f"MinIO Upload Error: {str(e)}")


async def delete_from_minio(url: str, bucket: str = MinioSettings.MINIO_BUCKET):
    try:
        idx = url.find(f"/{bucket}/")
        if idx == -1:
            raise ValueError(f"URL does not contain bucket name {bucket}")
        object_name = url[idx + len(f"/{bucket}/"):]
        if not minio_client.bucket_exists(bucket):
            raise ValueError(f"Bucket {bucket} does not exist.")
        minio_client.remove_object(bucket_name=bucket, object_name=object_name)
        return True
    except S3Error as e:
        print("MinIO Delete Error:", e)
        raise e
    except Exception as e:
        print("Delete from MinIO failed:", e)
        raise e