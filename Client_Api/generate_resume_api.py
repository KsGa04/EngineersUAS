import base64
import io
import os
from datetime import date
from time import sleep

from reportlab.lib.pagesizes import landscape, A4
from selenium import webdriver
from html2image import Html2Image
from reportlab.pdfgen import canvas
from flask import render_template, Blueprint, jsonify, make_response, send_file
import imgkit
from PIL import Image
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
        'pattern_resume1.html', user=user, profile_image=profile_image_base64,
        education_list=education_list, experience_list=experience_list, skills=skills,
        resume=resume, tasks_by_education=tasks_by_education, skills_by_task=skills_by_task,
        responsibilities_by_experience=responsibilities_by_experience, age=age_with_suffix,
        projects=projects, project_skills=project_skills
    )

    # Конфигурация Html2Image для сохранения изображения
    hti = Html2Image()
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Client_Server'))

    # Указание директории для CSS и изображений
    css_path = os.path.join(base_path, 'static/css/pattern_resume1.css')
    output_dir = os.path.join(base_path, 'templates')
    img_name = f'resume_{user_id}.png'

    # Установка output_path для сохранения в нужную директорию
    hti.output_path = output_dir
    hti.screenshot(html_str=rendered_html, css_file=css_path, save_as=img_name, size=(794, 1250))

    img_path = os.path.join(output_dir, img_name)

    # Отправка изображения пользователю
    return rendered_html


@resume_api.route('/pattern2/<int:user_id>', methods=['GET'])
def generate_resume_2(user_id):
    user = User.query.get_or_404(user_id)

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
        'pattern_resume2.html', user=user, profile_image=profile_image_base64,
        education_list=education_list, experience_list=experience_list, skills=skills,
        resume=resume, tasks_by_education=tasks_by_education, skills_by_task=skills_by_task,
        responsibilities_by_experience=responsibilities_by_experience, age=age_with_suffix,
        projects=projects, project_skills=project_skills
    )

    # Конфигурация Html2Image для сохранения изображения
    hti = Html2Image()
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Client_Server'))

    # Указание директории для CSS и изображений
    css_path = os.path.join(base_path, 'static/css/pattern_resume1.css')
    output_dir = os.path.join(base_path, 'templates')
    img_name = f'resume_{user_id}.png'

    # Установка output_path для сохранения в нужную директорию
    hti.output_path = output_dir
    hti.screenshot(html_str=rendered_html, css_file=css_path, save_as=img_name, size=(794, 1250))

    img_path = os.path.join(output_dir, img_name)

    # Отправка изображения пользователю
    return rendered_html

@resume_api.route('/pattern3/<int:user_id>', methods=['GET'])
def generate_resume_3(user_id):
    user = User.query.get_or_404(user_id)

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
        'pattern_resume3.html', user=user, profile_image=profile_image_base64,
        education_list=education_list, experience_list=experience_list, skills=skills,
        resume=resume, tasks_by_education=tasks_by_education, skills_by_task=skills_by_task,
        responsibilities_by_experience=responsibilities_by_experience, age=age_with_suffix,
        projects=projects, project_skills=project_skills
    )

    # Конфигурация Html2Image для сохранения изображения
    hti = Html2Image()
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../Client_Server'))

    # Указание директории для CSS и изображений
    css_path = os.path.join(base_path, 'static/css/pattern_resume1.css')
    output_dir = os.path.join(base_path, 'templates')
    img_name = f'resume_{user_id}.png'

    # Установка output_path для сохранения в нужную директорию
    hti.output_path = output_dir
    hti.screenshot(html_str=rendered_html, css_file=css_path, save_as=img_name, size=(794, 1250))

    img_path = os.path.join(output_dir, img_name)

    # Отправка изображения пользователю
    return rendered_html


@resume_api.route('/pattern_image_pdf/<int:user_id>', methods=['GET'])
def generate_resume_image_pdf(user_id):
    # Настраиваем Selenium для работы с Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-gpu')
    driver = webdriver.Chrome(options=options)

    # Открываем локальный сервер для рендеринга HTML
    url = f'http://127.0.0.1:5000/pattern1/{user_id}'
    driver.get(url)
    sleep(2)  # Ждем загрузки страницы и стилей

    # Устанавливаем альбомный размер для A4
    a4_width, a4_height = 860, 1350
    page_height = driver.execute_script("return document.body.scrollHeight")
    driver.set_window_size(a4_width, a4_height)  # Устанавливаем высоту окна по контенту

    # Сохраняем скриншот страницы как PNG
    tmp_dir = os.path.join(os.path.dirname(__file__), '../Client_Server/tmp')
    os.makedirs(tmp_dir, exist_ok=True)
    png_path = os.path.join(tmp_dir, f'resume_{user_id}.png')
    driver.save_screenshot(png_path)
    driver.quit()

    # Преобразование изображения в альбомный PDF с помощью ReportLab
    pdf_path = os.path.join(tmp_dir, f'resume_{user_id}.pdf')
    image = Image.open(png_path)

    # Подгонка изображения под размеры A4 (альбомный формат) без полей
    image = image.resize((a4_width, page_height), Image.LANCZOS)

    # Сохраняем изображение в PDF
    pdf_bytes = io.BytesIO()
    c = canvas.Canvas(pdf_bytes, pagesize=(a4_width, page_height))
    c.drawImage(png_path, 0, 0, width=a4_width, height=page_height)
    c.showPage()
    c.save()

    # Записываем PDF на диск
    with open(pdf_path, 'wb') as pdf_file:
        pdf_file.write(pdf_bytes.getvalue())

    # Отправка PDF пользователю
    return send_file(pdf_path, mimetype='application/pdf', as_attachment=True, download_name=f'resume_{user_id}.pdf')