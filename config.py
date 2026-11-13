import os
from pathlib import Path
from dotenv import load_dotenv

# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent

# Load environment variables from .env file if it exists
load_dotenv(BASE_DIR / ".env")

class Config:
    """Base application configuration."""
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-multi-disease-2026")
    
    # Database configuration for XAMPP MySQL
    DB_HOST = os.environ.get("DB_HOST", "localhost")
    DB_USER = os.environ.get("DB_USER", "root")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "")
    DB_NAME = os.environ.get("DB_NAME", "multi_disease_db")
    DB_PORT = int(os.environ.get("DB_PORT", 3306))
    
    # Upload Directories
    UPLOAD_FOLDER = BASE_DIR / "app" / "static" / "uploads"
    PLANT_UPLOAD_FOLDER = UPLOAD_FOLDER / "plant"
    CROP_UPLOAD_FOLDER = UPLOAD_FOLDER / "crop"
    SKIN_UPLOAD_FOLDER = UPLOAD_FOLDER / "skin"
    XRAY_UPLOAD_FOLDER = UPLOAD_FOLDER / "xray"
    BLOOD_REPORT_FOLDER = UPLOAD_FOLDER / "blood_reports"
    
    # Model Weights Folder
    MODELS_DIR = BASE_DIR / "ml_models"
    
    # Allowed file extensions for security
    ALLOWED_IMAGE_EXTENSIONS = {"png", "jpg", "jpeg"}
    ALLOWED_DOC_EXTENSIONS = {"pdf", "png", "jpg", "jpeg"}
    
    # Maximum upload size: 16 Megabytes
    MAX_CONTENT_LENGTH = int(os.environ.get("MAX_CONTENT_LENGTH", 16 * 1024 * 1024))
    
    # Session security
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"

