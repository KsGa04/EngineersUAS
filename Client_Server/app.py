from datetime import date

from flask import Flask, render_template
from flask_cors import CORS

from Client_Api.extensions import db, jwt  # Импортируем расширения
from Client_Api.auth_api import auth_api  # Подключаем API для авторизации
from Client_Server.config import Config  # Указываем полный путь до config
from flask_swagger_ui import get_swaggerui_blueprint
from Client_Api.generate_resume_api import resume_api
from Models import Education, WorkExperience, Skill, ResumeSkill, Resume, University, Task, TaskSkill, Project, \
    ProjectSkill, Responsibility
from Models.user import User
from Models.work import Work

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
app.register_blueprint(auth_api, url_prefix='/auth')  # Префикс для маршрутов авторизации
app.register_blueprint(resume_api, url_prefix='/api/resume')

@app.route('/')
def index():
    return render_template('main.html')

if __name__ == "__main__":
    CORS(app)
    app.run()
