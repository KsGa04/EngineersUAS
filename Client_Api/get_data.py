from flask import jsonify, Blueprint

from Client_Api.generate_resume_api import resume_api
from Models import Skill, Resume, ResumeSkill

get_api = Blueprint('get_api', __name__)
@get_api.route('/get/skills', methods=['GET'])
def get_skills():
    # Извлечение всех навыков из базы данных
    skills = Skill.query.all()

    # Преобразование данных в формат JSON
    skill_list = [{"id_skill": skill.id_skill, "skill_name": skill.skill_name} for skill in skills]

    return jsonify(skill_list)

@get_api.route('/api/student/<int:student_id>/skills', methods=['GET'])
def get_student_skills(student_id):
    # Находим резюме студента по его id
    resume = Resume.query.filter_by(id_user=student_id).first()

    if not resume:
        return jsonify({"error": "Resume not found for this student"}), 404

    # Получаем список навыков, связанных с этим резюме
    resume_skills = ResumeSkill.query.filter_by(id_resume=resume.id_resume).all()

    # Преобразуем в список навыков
    skills = [Skill.query.get(rs.id_skill).skill_name for rs in resume_skills]

    return jsonify({"student_id": student_id, "skills": skills})