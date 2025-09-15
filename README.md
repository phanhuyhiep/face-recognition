# ArcFace Face Recognition System
A comprehensive Python-based face recognition system implementing ArcFace with PyTorch, featuring user management, department organization, and secure file storage capabilities.

## Overview
This project combines the powerful ArcFace face recognition algorithm with a complete backend system for managing users, departments, and face data. It provides a RESTful API interface with JWT authentication and secure file storage using MinIO.

## Features
- **ArcFace Implementation**: PyTorch implementation of ArcFace for accurate face recognition
- **Face Recognition & Detection**: Real-time face detection and recognition capabilities
- **User Management System**: Complete user registration, authentication, and profile management
- **Department Organization**: Hierarchical department structure for user organization
- **JWT Authentication**: Secure token-based authentication system
- **Secure File Storage**: MinIO integration for scalable object storage
- **RESTful API**: Well-documented API endpoints for all functionalities
- **Database Integration**: MongoDB for flexible data storage

## Requirements
- Python 3.9+
- PyTorch
- MongoDB
- MinIO (Object Storage)

## ArcFace Model Information
- **Architecture**: ResNet-18 without SE blocks
- **Pretrained Model**: Available for download (see References section)
- **LFW Test Dataset**: Included for model evaluation

### Pretrained Model Download
The pretrained model and LFW test dataset can be downloaded from:
- **Link**: https://pan.baidu.com/s/1tFEX0yjUq3srop378Z1WMA
- **Password**: b2ec

**Note**: Please modify the path of the LFW dataset in `config.py` before running `test.py`.

## Configuration
The project uses the following configuration variables:

| Variable | Default Value | Description |
|----------|---------------|-------------|
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
cd arcface-face-recognition
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

# JWT Configuration
SECRET_KEY=suppersecretkey
ALGORITHM=HS256

# MongoDB Configuration
MONGO_USR=hiepph
MONGO_PWD=1
MONGO_HOST=localhost
MONGO_PORT=27017
MONGO_AUTH_SOURCE=face-recognition
MONGODB_NAME=face-recognition

# MongoDB Collections
COLLECTION_USER=collection_user
COLLECTION_DEPARTMENT=collection_department
COLLECTION_FACE=collection_face

# MinIO Configuration
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minio-access-key
MINIO_SECRET_KEY=minio-secret-key
MINIO_SECURE=False
MINIO_BUCKET=minio-bucket
```

### 5. Setup Dependencies
Ensure you have the following services running:
- **MongoDB**: Database server
- **MinIO**: Object storage server

### 6. Download Pretrained Models
1. Download the pretrained model and LFW dataset from the link provided above
2. Extract and place them in the appropriate directories
3. Update the dataset path in `config.py`

### 7. Run the application
```bash
# Activate virtual environment
source venv/bin/activate

# Start the application
python main.py

# Or if using FastAPI/uvicorn
uvicorn main:app --host localhost --port 8000 --reload
```

## Usage

### Testing the Model
```bash
# Run LFW evaluation
python test.py
```

### API Access
- **API Server**: `http://localhost:8000`
- **API Documentation**: `http://localhost:8000/docs` (if using FastAPI)

## References
This project is based on and inspired by the following repositories:
- https://github.com/deepinsight/insightface
- https://github.com/auroua/InsightFace_TF  
- https://github.com/MuggleWang/CosFace_pytorch

## License
https://hiepph.com

## Contributing
Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support
For questions and support, please refer to the project documentation or open an issue on the repository.
