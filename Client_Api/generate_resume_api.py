import base64
import io
import os
from datetime import date
from time import sleep

import requests
from PIL import Image
from flask import render_template, Blueprint, send_file, request, jsonify
from html2image import Html2Image
from reportlab.pdfgen import canvas
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from werkzeug.security import check_password_hash

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


def generate_resume_func(pattern_id, user_id, login, password):
    user = User.query.filter_by(email=login).first()

    if not user:
        return jsonify({'msg': 'User not found'}), 404

    if not check_password_hash(user.password, password):
        return jsonify({'msg': 'Invalid login or password'}), 401

    if user.id_user != user_id:
        return jsonify({'msg': 'User ID does not match'}), 404

    # Кодирование изображения профиля в Base64
    profile_image_base64 = None
    if user.profile_photo:
        profile_image_base64 = base64.b64encode(user.profile_photo).decode('utf-8')

    # Загрузка данных резюме и связанных элементов
    resume = Resume.query.filter_by(id_user=user_id).first_or_404()
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

    rendered_html = render_template(
        f'pattern_resume{pattern_id}.html', user=user, profile_image=profile_image_base64,
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