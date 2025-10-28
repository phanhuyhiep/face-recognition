import logging

from motor.motor_asyncio import AsyncIOMotorClient
from minio import Minio
from configs.minio_config import MinioSettings
from configs.mongodb_config import MongodbSettings


logger = logging.getLogger(__name__)


# --------- MongoDB ----------
try:
    mongo_client = AsyncIOMotorClient(MongodbSettings.MONGO_URI)
    db = mongo_client[MongodbSettings.MONGODB_NAME]
    collections = {
        name: db[coll_name]
        for name, coll_name in MongodbSettings.COLLECTIONS.items()
        if coll_name  # tránh None
    }
    collection_user = collections.get("user")
    collection_department = collections.get("department")
    collection_attendance = collections.get("attendance")
    collection_employee = collections.get("employee")

    logger.info(f"Connected to MongoDB: {MongodbSettings.MONGODB_NAME}")
    logger.info(f"Loaded collections: {list(collections.keys())}")

except Exception as e:
    logger.error(f"Failed to connect MongoDB: {e}")
    raise



# --------- MinIO ----------
minio_client = Minio(
    endpoint=MinioSettings.MINIO_ENDPOINT,
    access_key=MinioSettings.MINIO_ACCESS_KEY,
    secret_key=MinioSettings.MINIO_SECRET_KEY,
    secure=MinioSettings.MINIO_SECURE,
)

logger.info("Connected to MinIO")

if not minio_client.bucket_exists(MinioSettings.MINIO_BUCKET):
    minio_client.make_bucket(MinioSettings.MINIO_BUCKET)
