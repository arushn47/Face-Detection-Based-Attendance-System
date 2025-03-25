import os

# Base Directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Paths
FACE_DATA_PATH = os.path.join(BASE_DIR, "data", "face_data")
ATTENDANCE_PATH = os.path.join(BASE_DIR, "data", "attendance")
USER_CSV = os.path.join(BASE_DIR, "data", "users.csv")
DATABASE_JSON = os.path.join(BASE_DIR, "data", "database.json")

# Email Configuration
EMAIL_SENDER = "your-email@gmail.com"
EMAIL_PASSWORD = "your-email-password"
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
