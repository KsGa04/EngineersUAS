import json
from datetime import date

import requests
from flask import Flask, render_template, make_response, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from Client_Api.approach_to_universities import university_api
from Client_Api.extensions import db  # Импортируем расширения
from Client_Api.auth_api import auth_api  # Подключаем API для авторизации
from Client_Api.get_data import get_api
from Client_Api.get_github_repositories import github_api
from Client_Api.get_gitlab_repositories import gitlab_api
from Client_Api.get_user_data import get_user_api
from Client_Server.config import Config  # Указываем полный путь до config
from Client_Api.universal_api import universal_api
from flask_swagger_ui import get_swaggerui_blueprint
from Client_Api.generate_resume_api import resume_api


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.config["JWT_TOKEN_LOCATION"] = ["headers", "cookies"]
    app.config["JWT_COOKIE_SECURE"] = False  # Используйте True в продакшене
    app.config["JWT_ACCESS_COOKIE_NAME"] = "authToken"  # Название cookie для хранения токена
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB

    jwt = JWTManager(app)
    db.init_app(app)
    jwt.init_app(app)

    # Swagger
    SWAGGER_URL = '/swagger'
    API_URL = '/static/swagger.yml'  # Убедитесь, что swagger.yml находится в правильном месте

    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,
        API_URL,
        config={'app_name': "КИП API"}
    )
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    app.register_blueprint(auth_api)  # Префикс для маршрутов авторизации
    app.register_blueprint(resume_api)
    app.register_blueprint(universal_api)
    app.register_blueprint(get_api)
    app.register_blueprint(github_api, url_prefix='/api/github')
    app.register_blueprint(university_api)
    app.register_blueprint(gitlab_api, url_prefix='/api/gitlab')
    app.register_blueprint(get_user_api)

    app.secret_key = 'your_secret_key'


    return app

app = create_app(Config)

@app.route('/')
def index():
    return render_template('main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/userboard')
def userboard():
    return render_template('userboard.html')

@app.route('/set_cookie')
def set_cookie():
    response = make_response(jsonify({"msg": "Cookie set successfully"}))
    response.set_cookie('example_cookie', 'cookie_value', max_age=60*60*24)  # 1 день
    return response

@app.route('/get_cookie')
def get_cookie():
    cookie_value = request.cookies.get('example_cookie')
    if cookie_value:
        return jsonify({"msg": f"Cookie value: {cookie_value}"})
    return jsonify({"msg": "No cookie found"})

if __name__ == "__main__":
    CORS(app)
    app.run()
