from datetime import date

from flask import render_template, Blueprint, jsonify

from Client_Api.extensions import db
from Models import User, Education, Skills, ResumeSkills, Resume, Tasks, TaskSkills, Responsibility, \
    Projects, ProjectSkills
from Models.work import Work


def age_suffix(age):
    if 11 <= age % 100 <= 19:
        return "лет"
    elif age % 10 == 1:
        return "год"
    elif 2 <= age % 10 <= 4:
        return "года"
    else:
        return "лет"


resume_api = Blueprint('resume_api', __name__)


@resume_api.route('/pattern1/<int:user_id>', methods=['GET'])
def generate_resume(user_id):
    user = User.query.get_or_404(user_id)

    # Ищем резюме пользователя
    resume = Resume.query.filter_by(id_user=user_id).first_or_404()

    # Получение образования для данного резюме
    education_list = Education.query.filter_by(id_resume=resume.id_resume).all()

    # Получение опыта работы для данного резюме
    experience_list = Work.query.filter_by(id_resume=resume.id_resume).all()

    # Получение навыков через связь с резюме
    skills = db.session.query(Skills).join(ResumeSkills).filter(ResumeSkills.id_resume == resume.id_resume).all()

    # Получаем задачи и навыки для каждого образования по номеру группы
    tasks_by_education = {}
    skills_by_task = {}

    for education in education_list:
        group_number = education.group_number
        tasks = Tasks.query.filter_by(id_group=group_number).all()
        tasks_by_education[group_number] = tasks

        # Получение навыков для каждой задачи
        for task in tasks:
            task_skills = db.session.query(Skills).join(TaskSkills).filter(TaskSkills.id_task == task.id_task).all()
            skills_by_task[task.id_task] = task_skills

    # Добавляем обязанности для каждого опыта работы
    responsibilities_by_experience = {}

    for experience in experience_list:
        # Получаем обязанности, связанные с опытом работы
        responsibilities = Responsibility.query.filter_by(id_work=experience.id_work).all()
        responsibilities_by_experience[experience.id_work] = responsibilities

    projects = Projects.query.filter_by(id_resume=resume.id_resume).all()

    # Получение навыков для каждого проекта
    project_skills = {}
    for project in projects:
        skills_for_project = db.session.query(Skills).join(ProjectSkills).filter(
            ProjectSkills.id_project == project.id_project).all()
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
                           projects=projects, project_skills=project_skills, )
