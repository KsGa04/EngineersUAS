from flask import jsonify, Blueprint

from Models import Group, UniversityDirection, University

university_api = Blueprint('university_api', __name__)


@university_api.route('/get/universities', methods=['GET'])
def get_universities():
    # Извлечение всех университетов из базы данных
    universities = University.query.all()

    # Преобразование данных в формат JSON
    university_list = [{
        "id_university": university.id_university,
        "short_name": university.short_name,
        "full_name": university.full_name,
        "location": university.location,
        "website": university.website,
        "contact_info": university.contact_info
    } for university in universities]

    return jsonify(university_list), 200


@university_api.route('/get/university/<int:id_university>/directions', methods=['GET'])
def get_university_directions(id_university):
    # Получаем направления для конкретного университета по id_university
    directions = UniversityDirection.query.filter_by(id_university=id_university).all()

    if not directions:
        return jsonify({"msg": "No directions found for this university"}), 404

    # Преобразование данных в формат JSON
    direction_list = [{
        "id_direction": direction.direction.id_direction,
        "direction_code": direction.direction.direction_code,
        "direction_name": direction.direction.direction_name
    } for direction in directions]

    return jsonify(direction_list), 200


@university_api.route('/get/university/<int:id_university>/groups', methods=['GET'])
def get_university_groups(id_university):
    # Получаем группы для конкретного университета по id_university
    groups = Group.query.filter_by(id_university=id_university).all()

    if not groups:
        return jsonify({"msg": "No groups found for this university"}), 404

    # Преобразование данных в формат JSON
    group_list = [{
        "id_group": group.id_group,
        "group_name": group.group_name,
        "start_year": group.start_year,
        "id_direction": group.id_direction
    } for group in groups]

    return jsonify(group_list), 200
