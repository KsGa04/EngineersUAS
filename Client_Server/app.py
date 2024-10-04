from flask import Flask
from Client_Api.extensions import db, jwt  # Импортируем расширения
from Client_Api.auth_api import auth_api  # Подключаем API для авторизации
from Client_Server.config import Config  # Указываем полный путь до config
from flask_swagger_ui import get_swaggerui_blueprint

from Models.user import User

app = Flask(__name__)
app.config.from_object(Config)

# Инициализация базы данных и JWT
db.init_app(app)
jwt.init_app(app)

# Swagger
SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.yml'  # Убедитесь, что swagger.yml находится в правильном месте

swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "StudentSearch API"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

# Регистрируем все API из Client_Api
app.register_blueprint(auth_api, url_prefix='/api/auth')  # Префикс для маршрутов авторизации


@app.route('/users')
def get_users():
    with app.app_context():  # Контекст приложения для работы с базой данных
        # Получение всех пользователей
        users = User.query.all()

        # Преобразуем данные в читаемый формат (например, список словарей)
        users_list = [
            {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'phone': user.phone,
                'telegram_username': user.telegram_username,
                'city': user.city
            }
            for user in users
        ]

        return {'users': users_list}


if __name__ == "__main__":
    app.run(debug=True)
