# Face Recognition Project

A Python-based face recognition system with user management, department organization, and secure file storage capabilities.

## Requirements

- Python 3.9+
- MongoDB
- MinIO (Object Storage)

## Features

- Face recognition and detection
- User management system
- Department organization
- JWT authentication
- Secure file storage with MinIO
- RESTful API endpoints

## Configuration

The project uses the following configuration variables:

| Variable | Value | Description |
|----------|-------|-------------|
| **Core Settings** | | |
| `PORT` | `8000` | Application server port |
| `HOST` | `localhost` | Application server host |
| **JWT Authentication** | | |
| `SECRET_KEY` | `suppersecretkey` | JWT secret key for token signing |
| `ALGORITHM` | `HS256` | JWT algorithm |
| **MongoDB Configuration** | | |
| `MONGO_USR` | `hiepph` | MongoDB username |
| `MONGO_PWD` | `1` | MongoDB password |
| `MONGO_HOST` | `localhost` | MongoDB host |
| `MONGO_PORT` | `27017` | MongoDB port |
| `MONGO_AUTH_SOURCE` | `face-recognition` | MongoDB authentication database |
| `MONGODB_NAME` | `face-recognition` | Main database name |
| **MongoDB Collections** | | |
| `COLLECTION_USER` | `collection_user` | User data collection |
| `COLLECTION_DEPARTMENT` | `collection_department` | Department data collection |
| `COLLECTION_FACE` | `collection_face` | Face data collection |
| **MinIO Configuration** | | |
| `MINIO_ENDPOINT` | `localhost:9000` | MinIO server endpoint |
| `MINIO_ACCESS_KEY` | `minio-access-key` | MinIO access key |
| `MINIO_SECRET_KEY` | `minio-secret-key` | MinIO secret key |
| `MINIO_SECURE` | `False` | SSL/TLS connection (set to `True` for production) |
| `MINIO_BUCKET` | `minio-bucket` | Default storage bucket |

## Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd face-recognition-project
```

### 2. Create virtual environment
```bash
python3.9 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 4. Configure environment
Create a `.env` file in the project root with your configuration:
```env
PORT=8000
HOST=localhost
SECRET_KEY=suppersecretkey
ALGORITHM=HS256
MONGO_USR=hiepph
MONGO_PWD=1
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_AUTH_SOURCE=face-recognition
MONGODB_NAME=face-recognition
COLLECTION_USER=collection_user
COLLECTION_DEPARTMENT=collection_department
COLLECTION_FACE=collection_face
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minio-access-key
MINIO_SECRET_KEY=minio-secret-key
MINIO_SECURE=False
MINIO_BUCKET=minio-bucket
```
### 5. Run the application
```bash
# Activate virtual environment
source venv/bin/activate

# Start the application
python main.py
# Or if using FastAPI/uvicorn
uvicorn main:app --host localhost --port 8000 --reload
```

### 6. Access the application
- API Server: `http://localhost:8000`
- API Documentation (if using FastAPI): `http://localhost:8000/docs`

## License

https:hiepph.com

## Contributing

.....