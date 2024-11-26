from functools import wraps

from flask import Flask, render_template, make_response, jsonify, request, redirect, url_for
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, verify_jwt_in_request, get_jwt
from werkzeug.security import generate_password_hash

from Client_Api.approach_to_universities import university_api
from Client_Api.extensions import db  # Импортируем расширения
from Client_Api.auth_api import auth_api  # Подключаем API для авторизации
from Client_Api.get_data import get_api
from Client_Api.get_github_repositories import github_api
from Client_Api.get_gitlab_repositories import gitlab_api
from Client_Api.get_user_data import get_user_api
from Client_Api.project_api import modal_api
from config import Config  # Указываем полный путь до config
from Client_Api.universal_api import universal_api
from flask_swagger_ui import get_swaggerui_blueprint
from Client_Api.generate_resume_api import resume_api
from Admin.admin import admin_login, is_admin

def role_required(required_role_id):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            verify_jwt_in_request()
            jwt_data = get_jwt()
            user_role_id = jwt_data.get("role_id")
            if user_role_id != required_role_id:
                return jsonify({"msg": "Access forbidden: You do not have the required role"}), 403
            return fn(*args, **kwargs)
        return wrapper
    return decorator

def create_app(config):
    global SWAGGER_URL

    app = Flask(__name__)
    app.secret_key = 'kip_secret_key_123'
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
    app.register_blueprint(modal_api)
    app.register_blueprint(admin_login)

    app.secret_key = 'your_secret_key'


    return app, jwt

app, jwt = create_app(Config)
CORS(app)
CORS(app, resources={r"/pattern_image_pdf/*": {"origins": "*"}})
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/hr')
def hr():
    return render_template('hr_main.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/userboard')
@jwt_required()
@role_required(1)
def userboard():
    return render_template('userboard.html')

@app.route('/cvgenerator')
@jwt_required()
@role_required(1)
def cv_generator():
    return render_template('cv_generation.html')

@app.route('/analytics')
@jwt_required()
@role_required(2)
def analytics():
    return render_template('analytics.html')

@app.route('/candidats')
@jwt_required()
@role_required(2)
def candidats():
    return render_template('hr_page.html')

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

@app.before_request
def restrict_swagger_access():
    if request.path.startswith(SWAGGER_URL) and not is_admin():
        return redirect(url_for('admin_login.admin_login_func'))

@app.errorhandler(401)
def not_logged_in_error(error):
    return redirect(url_for('login'))

@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
