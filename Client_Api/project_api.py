# ================= API для Проекты =================
from flask import jsonify, request, Blueprint
from langfuse.api import Project

from Client_Api.extensions import db
from Models import UserSocialNetwork, Education, Skills, University, Direction, Group, Degree
from Models.work import Work

modal_api = Blueprint('modal_api', __name__)


@modal_api.route('/api/work', methods=['POST'])
def add_work_experience():
    data = request.json
    new_work = Work(
        id_resume=data['id_resume'],
        position=data['position'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_work)
    db.session.commit()
    return jsonify({"message": "Опыт работы добавлен"}), 201


@modal_api.route('/api/work/<int:id>', methods=['PUT'])
def update_work_experience(id):
    data = request.json
    work = Work.query.get(id)
    if not work:
        return jsonify({"error": "Опыт работы не найден"}), 404
    work.position = data.get('position', work.position)
    work.start_date = data.get('start_date', work.start_date)
    work.end_date = data.get('end_date', work.end_date)
    db.session.commit()
    return jsonify({"message": "Опыт работы обновлен"}), 200


@modal_api.route('/api/work/<int:id>', methods=['DELETE'])
def delete_work_experience(id):
    work = Work.query.get(id)
    if not work:
        return jsonify({"error": "Опыт работы не найден"}), 404
    db.session.delete(work)
    db.session.commit()
    return jsonify({"message": "Опыт работы удален"}), 200


# ================= API для Образование =================
@modal_api.route('/api/education', methods=['POST'])
def add_education():
    data = request.json
    new_education = Education(
        id_resume=data['id_resume'],
        id_university=data['id_university'],
        id_degree=data['id_degree'],
        start_date=data['start_date'],
        end_date=data['end_date']
    )
    db.session.add(new_education)
    db.session.commit()
    return jsonify({"message": "Образование добавлено"}), 201


@modal_api.route('/api/education/<int:id>', methods=['PUT'])
def update_education(id):
    data = request.json
    education = Education.query.get(id)
    if not education:
        return jsonify({"error": "Образование не найдено"}), 404
    education.start_date = data.get('start_date', education.start_date)
    education.end_date = data.get('end_date', education.end_date)
    db.session.commit()
    return jsonify


@modal_api.route('/api/project', methods=['POST'])
def add_project():
    data = request.json
    new_project = Project(
        id_resume=data['id_resume'],
        project_name=data['project_name'],
        project_description=data['project_description'],
        project_link=data['project_link']
    )
    db.session.add(new_project)
    db.session.commit()
    return jsonify({"message": "Проект добавлен"}), 201


@modal_api.route('/api/project/<int:id>', methods=['PUT'])
def update_project(id):
    data = request.json
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Проект не найден"}), 404
    project.project_name = data.get('project_name', project.project_name)
    project.project_description = data.get('project_description', project.project_description)
    project.project_link = data.get('project_link', project.project_link)
    db.session.commit()
    return jsonify({"message": "Проект обновлен"}), 200


@modal_api.route('/api/project/<int:id>', methods=['DELETE'])
def delete_project(id):
    project = Project.query.get(id)
    if not project:
        return jsonify({"error": "Проект не найден"}), 404
    db.session.delete(project)
    db.session.commit()
    return jsonify({"message": "Проект удален"}), 200


# ================= API для Навыки =================
@modal_api.route('/api/skills', methods=['POST'])
def add_skill():
    data = request.json
    new_skill = Skills(
        skill_name=data['skill_name']
    )
    db.session.add(new_skill)
    db.session.commit()
    return jsonify({"message": "Навык добавлен"}), 201


@modal_api.route('/api/skills/<int:id>', methods=['PUT'])
def update_skill(id):
    data = request.json
    skill = Skills.query.get(id)
    if not skill:
        return jsonify({"error": "Навык не найден"}), 404
    skill.skill_name = data.get('skill_name', skill.skill_name)
    db.session.commit()
    return jsonify({"message": "Навык обновлен"}), 200


@modal_api.route('/api/skills/<int:id>', methods=['DELETE'])
def delete_skill(id):
    skill = Skills.query.get(id)
    if not skill:
        return jsonify({"error": "Навык не найден"}), 404
    db.session.delete(skill)
    db.session.commit()
    return jsonify({"message": "Навык удален"}), 200


# ================= API для Ссылки на портфолио =================
@modal_api.route('/api/social_link', methods=['POST'])
def add_social_link():
    data = request.json
    new_social_link = UserSocialNetwork(
        id_resume=data['id_resume'],
        id_social_network_type=data['id_social_network_type'],
        network_link=data['network_link']
    )
    db.session.add(new_social_link)
    db.session.commit()
    return jsonify({"message": "Ссылка на портфолио добавлена"}), 201


@modal_api.route('/api/social_link/<int:id>', methods=['PUT'])
def update_social_link(id):
    data = request.json
    social_link = UserSocialNetwork.query.get(id)
    if not social_link:
        return jsonify({"error": "Ссылка не найдена"}), 404
    social_link.network_link = data.get('network_link', social_link.network_link)
    db.session.commit()
    return jsonify({"message": "Ссылка обновлена"}), 200


@modal_api.route('/api/social_link/<int:id>', methods=['DELETE'])
def delete_social_link(id):
    social_link = UserSocialNetwork.query.get(id)
    if not social_link:
        return jsonify({"error": "Ссылка не найдена"}), 404
    db.session.delete(social_link)
    db.session.commit()
    return jsonify({"message": "Ссылка удалена"}), 200

# Эндпоинт для получения списка университетов
@modal_api.route('/api/universities', methods=['GET'])
def get_universities():
    universities = University.query.all()
    university_list = [{"id": u.id_university, "name": u.full_name} for u in universities]
    return jsonify(university_list)

# Эндпоинт для получения групп по ID направления
@modal_api.route('/api/groups', methods=['GET'])
def get_groups():
    # Получение параметров запроса
    university_id = request.args.get('university_id', type=int)
    direction_id = request.args.get('direction_id', type=int)

    # Построение запроса с учетом фильтров
    query = Group.query
    if university_id:
        query = query.filter_by(id_university=university_id)
    if direction_id:
        query = query.filter_by(id_direction=direction_id)

    # Получение отфильтрованных данных
    groups = query.all()
    group_list = [{"id": g.id_group, "name": g.group_name} for g in groups]
    return jsonify(group_list), 200

@modal_api.route('/api/degrees', methods=['GET'])
def get_degrees():
    degrees = Degree.query.all()
    degree_list = [{"id": d.id_degree, "name": d.degree_name} for d in degrees]
    return jsonify(degree_list)
