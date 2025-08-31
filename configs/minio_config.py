import os
from dotenv import load_dotenv

load_dotenv()


class MinioSettings:
    MINIO_ENDPOINT = os.environ.get("MINIO_ENDPOINT", "localhost:9000")
    MINIO_ACCESS_KEY = os.environ.get("MINIO_ACCESS_KEY", "admin")
    MINIO_SECRET_KEY = os.environ.get("MINIO_SECRET_KEY", "admin123")
    MINIO_SECURE = os.environ.get("MINIO_SECURE", "false").lower() == "true"
    MINIO_BUCKET = os.environ.get("MINIO_BUCKET", "faces")



