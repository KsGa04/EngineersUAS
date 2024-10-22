from flask import jsonify, Blueprint

from Client_Api.extensions import db
from Client_Api.generate_resume_api import resume_api
from Models import Skills, Resume, ResumeSkills, TaskSkills, ProjectSkills

get_api = Blueprint('get_api', __name__)


@get_api.route('/get/skills', methods=['GET'])
def get_skills():
    # Извлечение всех навыков из базы данных
    skills = Skills.query.all()

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
    resume_skills = ResumeSkills.query.filter_by(id_resume=resume.id_resume).all()

    # Преобразуем в список навыков
    skills = [Skills.query.get(rs.id_skill).skill_name for rs in resume_skills]

    return jsonify({"student_id": student_id, "skills": skills})


# Получить навыки проекта по id проекта
@get_api.route('/api/project/<int:id_project>/skills', methods=['GET'])
def get_project_skills(id_project):
    try:
        # Извлекаем навыки, связанные с проектом
        skills = db.session.query(Skills).join(ProjectSkills).filter(ProjectSkills.id_project == id_project).all()
        skill_list = [{"id_skill": skill.id_skill, "skill_name": skill.skill_name} for skill in skills]
        return jsonify(skill_list), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400


# Получить навыки по задаче
@get_api.route('/api/task/<int:id_task>/skills', methods=['GET'])
def get_task_skills(id_task):
    try:
        # Извлекаем навыки, связанные с задачей
        skills = db.session.query(Skills).join(TaskSkills).filter(TaskSkills.id_task == id_task).all()
        skill_list = [{"id_skill": skill.id_skill, "skill_name": skill.skill_name} for skill in skills]
        return jsonify(skill_list), 200
    except Exception as e:
        return jsonify({"msg": str(e)}), 400
