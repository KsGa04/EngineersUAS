import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-jwt-key')

    # Production database URI
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'mysql+mysqlconnector://root@localhost:3306/engineersuas_db')

    # Test database URI
    SQLALCHEMY_DATABASE_URI_TEST = os.getenv('DATABASE_URL_TEST',
                                             'mysql+mysqlconnector://root@localhost:3306/engineersuas_test')

    SQLALCHEMY_TRACK_MODIFICATIONS = False
