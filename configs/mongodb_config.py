import os
from dotenv import load_dotenv

load_dotenv()

class MongodbSettings: 
    MONGO_USR= os.environ.get('MONGO_USR')
    MONGO_PWD= os.environ.get('MONGO_PWD')
    MONGO_HOST= os.environ.get('MONGO_HOST')
    MONGO_PORT= os.environ.get('MONGO_PORT')
    MONGO_AUTH_SOURCE= os.environ.get('MONGO_AUTH_SOURCE')
    MONGODB_NAME = os.environ.get('MONGODB_NAME')


    MONGO_URI = "mongodb://{}:{}@{}:{}/?authSource={}&directConnection=true".format(
        MONGO_USR, MONGO_PWD, MONGO_HOST, MONGO_PORT, MONGO_AUTH_SOURCE
    )

    COLLECTIONS = {
        "user": os.environ.get("COLLECTION_USER"),
        "department": os.environ.get("COLLECTION_DEPARTMENT"),
        "face": os.environ.get("COLLECTION_FACE"),
    }

required_vars = [
    "MONGO_USR", "MONGO_PWD", "MONGO_HOST",
    "MONGO_PORT", "MONGO_AUTH_SOURCE", "MONGODB_NAME"
]

for var in required_vars:
    if not getattr(MongodbSettings, var):
        raise ValueError(f"Missing required environment variable: {var}")