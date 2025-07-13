import os
from urllib.parse import quote_plus

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a8f5f167f44f4964e6c998dee827110c'
    
    # Database configuration
    DB_USER = os.getenv('DB_USER', 'root')
    DB_PASSWORD = quote_plus(os.getenv('DB_PASSWORD', '123456')) 
    DB_NAME = os.getenv('DB_NAME', 'STOCK_HOLM')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f'mysql+pymysql://{DB_USER}:{DB_PASSWORD}@localhost/{DB_NAME}'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
