import os

class Config:
    UPLOAD_FOLDER = './uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'docx','MP4'}
    SECRET_KEY = 'rdx'  # Replace with a real secret key for production
    SQLALCHEMY_DATABASE_URI = 'sqlite:///database.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

