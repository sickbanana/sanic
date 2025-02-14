import os

JWT_SECRET = os.environ.get('JWT_SECRET')

SECRET_KEY = os.environ.get('SECRET_KEY')

POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

POSTGRES_HOST = os.environ.get('POSTGRES_HOST')

connection = f"postgresql://postgres:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/postgres"