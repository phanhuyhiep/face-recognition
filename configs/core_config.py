import os
from dotenv import load_dotenv

load_dotenv()


class CoreSettings:
    PORT = int(os.environ.get("PORT", 8000))
    HOST = os.environ.get("HOST", "localhost")
    SECRET_KEY = os.environ.get("SECRET_KEY", "suppersecretkey")
    ALGORITHM = os.environ.get("ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES = 10080 # 7 days


