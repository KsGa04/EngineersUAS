import os


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'super-secret-key')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'super-secret-jwt-key')

    # Production database URI
    SQLALCHEMY_DATABASE_URI = r"mysql+mysqlconnector://gen_user:1\}&\/N\j2-\xL@185.247.185.50:3306/default_db"

    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_size": 10,  # Начальный размер пула соединений
        "pool_timeout": 30,  # Время ожидания свободного соединения (в секундах)
        "pool_recycle": 1800,  # Обновление соединения каждые 30 минут
        "pool_pre_ping": True  # Проверка соединения перед его использованием
    }

    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    TESTING = True
    # Используйте тестовую базу данных
    SQLALCHEMY_DATABASE_URI = r"mysql+mysqlconnector://gen_user:1\}&\/N\j2-\xL@185.247.185.50:3306/kip_test_db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False