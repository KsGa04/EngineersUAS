from flask import render_template

from Client_Api.extensions import db
from Client_Server.app import app
from Models import User, Education, WorkExperience, Skill, ResumeSkill, Resume
from Models.work import Work


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

    # Рендеринг HTML-шаблона с полученными данными
    return render_template('resume_template.html', user=user, education_list=education_list,
                           experience_list=experience_list, skills=skills)

