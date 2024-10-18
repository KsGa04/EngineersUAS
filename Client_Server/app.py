from datetime import date

from flask import Flask, render_template
from flask_cors import CORS

from Client_Api.extensions import db, jwt  # Импортируем расширения
from Client_Api.auth_api import auth_api  # Подключаем API для авторизации
from Client_Server.config import Config  # Указываем полный путь до config
from flask_swagger_ui import get_swaggerui_blueprint

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

def age_suffix(age):
    if 11 <= age % 100 <= 19:
        return "лет"
    elif age % 10 == 1:
        return "год"
    elif 2 <= age % 10 <= 4:
        return "года"
    else:
        return "лет"


@app.route('/resume/<int:user_id>')
def generate_resume(user_id):
    # Получаем пользователя по user_id
    user = User.query.get_or_404(user_id)

    # Ищем резюме пользователя
    resume = Resume.query.filter_by(id_user=user_id).first_or_404()

    # Получение образования для данного резюме
    education_list = Education.query.filter_by(id_resume=resume.id_resume).all()

    # Получение опыта работы для данного резюме
    experience_list = Work.query.filter_by(id_resume=resume.id_resume).all()

    # Получение навыков через связь с резюме
    skills = db.session.query(Skill).join(ResumeSkill).filter(ResumeSkill.id_resume == resume.id_resume).all()

    # Получаем задачи и навыки для каждого образования по номеру группы
    tasks_by_education = {}
    skills_by_task = {}

    for education in education_list:
        group_number = education.group_number
        tasks = Task.query.filter_by(id_group=group_number).all()
        tasks_by_education[group_number] = tasks

        # Получение навыков для каждой задачи
        for task in tasks:
            task_skills = db.session.query(Skill).join(TaskSkill).filter(TaskSkill.id_task == task.id_task).all()
            skills_by_task[task.id_task] = task_skills

    # Добавляем обязанности для каждого опыта работы
    responsibilities_by_experience = {}

    for experience in experience_list:
        # Получаем обязанности, связанные с опытом работы
        responsibilities = Responsibility.query.filter_by(id_work=experience.id_work).all()
        responsibilities_by_experience[experience.id_work] = responsibilities

    projects = Project.query.filter_by(id_resume=resume.id_resume).all()

    # Получение навыков для каждого проекта
    project_skills = {}
    for project in projects:
        skills_for_project = db.session.query(Skill).join(ProjectSkill).filter(
            ProjectSkill.id_project == project.id_project).all()
        project_skills[project.id_project] = skills_for_project

    # Вычисляем возраст
    today = date.today()
    birth_date = user.birth_date
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    age_with_suffix = f"{age} {age_suffix(age)}"

    # Рендеринг шаблона с переданными данными
    return render_template('pattern_resume1.html', user=user, education_list=education_list,
                           experience_list=experience_list, skills=skills, resume=resume,
                           tasks_by_education=tasks_by_education, skills_by_task=skills_by_task,
                           responsibilities_by_experience=responsibilities_by_experience, age=age_with_suffix,
                           projects=projects, project_skills=project_skills,)



if __name__ == "__main__":
    CORS(app)
    app.run()
