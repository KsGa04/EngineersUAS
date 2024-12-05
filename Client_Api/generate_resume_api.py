import base64
import io
import os
from datetime import date
from time import sleep

import requests
from PIL import Image
from flask import render_template, Blueprint, send_file, request, jsonify
from html2image import Html2Image
from langchain_core.messages import SystemMessage
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from werkzeug.security import check_password_hash
from flask_jwt_extended import get_jwt_identity, jwt_required
from langchain_community.chat_models import GigaChat
from Client_Api.extensions import db
from Models import User, Education, Skills, ResumeSkills, Resume, Tasks, TaskSkills, Responsibility, \
    Projects, ProjectSkills, UserSocialNetwork
from Models.work import Work
from Admin.admin import is_admin

# Инициализация GigaChat
giga = GigaChat(
    credentials="N2Q2MjFiYmUtN2IwNy00ODNhLTk3MGQtOTUyNmQyYjAyNTY1Ojg4MzBkMmIwLThlMzItNDQyNi1hYzI1LTQ0ZmI0MWVkYmI2Mg==",
    scope="GIGACHAT_API_PERS", verify_ssl_certs=False, streaming=True
)


def generate_description(education_list, skills, experience_list):
    # Формируем описание образования с использованием связанных данных
    education_descriptions = "; ".join([
        f"{edu.degree.degree_name} по направлению {edu.direction.direction_name} в {edu.university.full_name} "
        f"({edu.start_date.year} - {edu.end_date.year if edu.end_date else 'н.в.'})"
        for edu in education_list
    ])

    # Формируем описание навыков
    skill_descriptions = ", ".join([skill.skill_name for skill in skills])

    # Формируем описание опыта работы с учётом организации
    experience_descriptions = "; ".join([
        f"{exp.position} в {', '.join([org.organization_name for org in exp.organizations])} "
        f"({exp.start_date.year}-{exp.end_date.year if exp.end_date else 'н.в.'})"
        for exp in experience_list
    ])

    # Создаем сообщение для модели
    messages = [
        SystemMessage(
            content=(
                f"Сгенерируй описание профиля на 15 слов на русском языке как будто ты инженер. Образование: {education_descriptions}. "
                f"Навыки: {skill_descriptions}. Опыт работы: {experience_descriptions}. "
            )
        )
    ]

    # Вызов модели с сообщением
    res = giga(messages)

    # Возвращаем сгенерированный текст
    return res.content


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

@jwt_required()
def generate_resume_func(pattern_id, user_id, login, password):
    user = User.query.get_or_404(user_id)
    current_user = int(get_jwt_identity())

    if user_id != current_user and not current_user == 'admin':
        return jsonify({'msg': 'User not found'}), 401

    # Кодирование изображения профиля в Base64
    profile_image_base64 = None
    if user.profile_photo:
        profile_image_base64 = base64.b64encode(user.profile_photo).decode('utf-8')

    # Загрузка данных резюме и связанных элементов
    resume = Resume.query.filter_by(id_user=user_id).first_or_404()
    telegram = UserSocialNetwork.query.filter(UserSocialNetwork.id_resume == resume.id_resume, UserSocialNetwork.network_link.startswith("https://t.me/")).first_or_404()
    education_list = Education.query.filter_by(id_resume=resume.id_resume).all()
    experience_list = Work.query.filter_by(id_resume=resume.id_resume).all()
    skills = db.session.query(Skills).join(ResumeSkills).filter(ResumeSkills.id_resume == resume.id_resume).all()
    tasks_by_education, skills_by_task, responsibilities_by_experience, project_skills = {}, {}, {}, {}

    for education in education_list:
        group_number = education.group_number
        tasks = Tasks.query.filter_by(id_group=group_number).all()
        tasks_by_education[group_number] = tasks
        for task in tasks:
            task_skills = db.session.query(Skills).join(TaskSkills).filter(TaskSkills.id_task == task.id_task).all()
            skills_by_task[task.id_task] = task_skills

    for experience in experience_list:
        responsibilities = Responsibility.query.filter_by(id_work=experience.id_work).all()
        responsibilities_by_experience[experience.id_work] = responsibilities

    projects = Projects.query.filter_by(id_resume=resume.id_resume).all()
    for project in projects:
        skills_for_project = db.session.query(Skills).join(ProjectSkills).filter(
            ProjectSkills.id_project == project.id_project).all()
        project_skills[project.id_project] = skills_for_project

    today = date.today()
    age = today.year - user.birth_date.year - ((today.month, today.day) < (user.birth_date.month, user.birth_date.day))
    age_with_suffix = f"{age} {age_suffix(age)}"
    if resume.about_me == "":
        # Генерируем описание профиля
        resume.about_me = generate_description(education_list, skills, experience_list)
        db.session.commit()

    rendered_html = render_template(
            f'pattern_resume{pattern_id}.html', telegram=telegram.network_link, user=user, profile_image=profile_image_base64,
            education_list=education_list, experience_list=experience_list, skills=skills,
            resume=resume, tasks_by_education=tasks_by_education, skills_by_task=skills_by_task,
            responsibilities_by_experience=responsibilities_by_experience, age=age_with_suffix,
            projects=projects, project_skills=project_skills
        )
    # Отправка изображения пользователю
    return rendered_html

@resume_api.route('/pattern1/<int:user_id>', methods=['GET'])
def generate_resume(user_id):
    return generate_resume_func(1, user_id, request.args.get('login'), request.args.get('password'))


@resume_api.route('/pattern2/<int:user_id>', methods=['GET'])
def generate_resume_2(user_id):
    return generate_resume_func(2, user_id, request.args.get('login'), request.args.get('password'))

@resume_api.route('/pattern3/<int:user_id>', methods=['GET'])
def generate_resume_3(user_id):
    return generate_resume_func(3, user_id, request.args.get('login'), request.args.get('password'))


def generate_image_from_url(url):
    api_key = 'your_apiflash_api_key'
    response = requests.get(
        f"https://api.apiflash.com/v1/urltoimage?access_key={api_key}&url={url}"
    )
    if response.status_code == 200:
        with open("screenshot.png", "wb") as file:
            file.write(response.content)
    else:
        print("Ошибка генерации изображения:", response.text)


@resume_api.route('/pattern_image_pdf/<int:user_id>/<int:id_pattern>', methods=['GET'])
def generate_resume_image_pdf(user_id, id_pattern):
    url = f'http://46.229.215.18:5000/pattern_image_pdf/{user_id}/{id_pattern}'
    response = requests.get(url)

    if response.status_code == 200:
        # Сохранение PDF-файла временно
        pdf_path = f'tmp_resume_{user_id}.pdf'
        with open(pdf_path, 'wb') as f:
            f.write(response.content)

        # Отправка PDF-файла клиенту
        return send_file(pdf_path, mimetype='application/pdf', as_attachment=True,
                         download_name=f'resume_{user_id}.pdf')
    else:
        return jsonify({'error': f'Failed to fetch PDF: {response.status_code}, {response.text}'}), response.status_code