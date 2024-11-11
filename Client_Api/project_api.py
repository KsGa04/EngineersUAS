# ================= API для Проекты =================
import base64
from datetime import datetime

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from langfuse.api import Project
from sqlalchemy.orm import joinedload

from Client_Api.extensions import db
from Models import UserSocialNetwork, Education, Skills, University, Direction, Group, Degree, Organization, User, \
    Resume, ResumeSkills, Projects, WorkOrganization
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

@modal_api.route('/api/organizations', methods=['GET'])
def get_organization():
    organizations = Organization.query.all()
    organizations_list = [{"id": u.id_organization, "name": u.organization_name} for u in organizations]
    return jsonify(organizations_list)

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

@modal_api.route('/api/directions', methods=['GET'])
def get_directions():
    directions = Direction.query.all()
    directions_list = [{"id": d.id_direction, "name": d.direction_name} for d in directions]
    return jsonify(directions_list)

@modal_api.route('/api/projects', methods=['GET'])
def get_projects():
    projects = Projects.query.all()
    projects_list = [{"id": d.id_project, "name": d.project_name} for d in projects]
    return jsonify(projects_list)

@modal_api.route('/api/candidates', methods=['GET'])
def get_candidates():
    candidates = []

    users = User.query.filter_by(role_id=1).all()

    for user in users:
        # Проверка, что поле profile_photo содержит данные
        if user.profile_photo:
            # Кодирование бинарных данных в base64
            profile_photo_encoded = base64.b64encode(user.profile_photo).decode('utf-8')
            profile_photo_data = f"data:image/jpeg;base64,{profile_photo_encoded}"
        else:
            profile_photo_data = None

        candidate_data = {
            'id_user': user.id_user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'email': user.email,
            'phone': user.phone,
            'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
            'address': user.address,
            'profile_photo': profile_photo_data,
            'resumes': []
        }

        resumes = Resume.query.filter_by(id_user=user.id_user).all()

        for resume in resumes:
            resume_data = {
                'id_resume': resume.id_resume,
                'about_me': resume.about_me,
                'id_pattern': resume.id_pattern,
                'educations': [],
                'skills': []
            }

            educations = Education.query.filter_by(id_resume=resume.id_resume).all()
            for edu in educations:
                education_data = {
                    'id_education': edu.id_education,
                    'university_name': edu.university.full_name if edu.university else None,
                    'direction_name': edu.direction.direction_name if edu.direction else None,
                    'city': edu.university.location if edu.university else None,
                }
                resume_data['educations'].append(education_data)

            resume_skills = ResumeSkills.query.filter_by(id_resume=resume.id_resume).all()
            for rs in resume_skills:
                skill = Skills.query.get(rs.id_skill)
                if skill:
                    resume_data['skills'].append({
                        'id_skill': skill.id_skill,
                        'skill_name': skill.skill_name
                    })

            candidate_data['resumes'].append(resume_data)

        candidates.append(candidate_data)

    return jsonify(candidates)


@modal_api.route('/api/regions', methods=['GET'])
def get_regions():
    try:
        # Получаем все адреса пользователей
        user_addresses = db.session.query(User.address).filter(User.address.isnot(None)).all()
        # Получаем все локации университетов
        university_locations = db.session.query(University.location).filter(University.location.isnot(None)).all()
        # Получаем все локации организаций
        organization_locations = db.session.query(Organization.location).filter(Organization.location.isnot(None)).all()

        # Преобразуем полученные кортежи в плоский список
        all_locations = {addr[0] for addr in user_addresses + university_locations + organization_locations}

        # Убираем пустые значения, если они есть
        all_locations = list(filter(None, all_locations))

        return jsonify(sorted(all_locations))  # Сортируем для удобства просмотра
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@modal_api.route('/api/educations/<int:id_resume>', methods=['GET'])
@jwt_required()  # Требуем наличие JWT
def get_educations_by_resume(id_resume):
    current_user_id = get_jwt_identity()

    # Check if the resume belongs to the current user
    resume = Resume.query.filter_by(id_resume=id_resume, id_user=current_user_id).first()
    if not resume:
        return jsonify({"msg": "Access denied or resume not found"}), 403

    educations = Education.query.filter_by(id_resume=id_resume).all()
    education_list = []

    for edu in educations:
        university_name = edu.university.full_name if edu.university else None
        degree_name = edu.degree.degree_name if edu.degree else None
        group_name = Group.query.filter_by(id_group=edu.group_number).first().group_name if edu.group_number else None

        education_data = {
            'id_education': edu.id_education,
            'university_name': university_name,
            'degree_name': degree_name,
            'group_name': group_name,
            'start_date': edu.start_date.strftime('%Y-%m-%d') if edu.start_date else None,
            'end_date': edu.end_date.strftime('%Y-%m-%d') if edu.end_date else None
        }
        education_list.append(education_data)

    return jsonify(education_list), 200

@modal_api.route('/api/education/<int:id_user>/<int:id_education>', methods=['GET'])
@jwt_required()  # Requires JWT for authentication
def get_education_detail(id_user, id_education):
    current_user_id = get_jwt_identity()

    # Verify that the requested user matches the authenticated user
    if current_user_id != id_user:
        return jsonify({"msg": "Access denied"}), 403

    education = Education.query.filter_by(id_education=id_education).join(Resume).filter(Resume.id_user == id_user).first()
    if not education:
        return jsonify({"msg": "Education not found"}), 404

    education_data = {
        'id_education': education.id_education,
        'university_id': education.id_university,
        'university_name': education.university.full_name if education.university else None,
        'degree_id': education.id_degree,
        'degree_name': education.degree.degree_name if education.degree else None,
        'direction_id': education.id_direction,
        'direction_name': education.direction.direction_name if education.direction else None,
        'group_id': education.group_number,
        'group_name': Group.query.filter_by(id_group=education.group_number).first().group_name if education.group_number else None,
        'start_date': education.start_date.strftime('%Y-%m-%d') if education.start_date else None,
        'end_date': education.end_date.strftime('%Y-%m-%d') if education.end_date else None
    }

    return jsonify(education_data), 200

@modal_api.route('/api/education/<int:id_user>', methods=['POST'])
def add_education(id_user):
    resume = Resume.query.filter_by(id_user=id_user).first()
    if not resume:
        return jsonify({"msg": "Resume for user not found"}), 404

    data = request.get_json()

    # Check that all required fields are provided
    required_fields = ['university', 'degree', 'direction', 'group', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    try:
        new_education = Education(
            id_resume=resume.id_resume,
            id_university=int(data['university']),
            id_degree=int(data['degree']),
            id_direction=int(data['direction']),
            group_number=int(data['group']),
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d')
        )

        db.session.add(new_education)
        db.session.commit()
        return jsonify({"msg": "Education added successfully", "id_education": new_education.id_education}), 201

    except ValueError as ve:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to add education: {str(e)}"}), 500


@modal_api.route('/api/education/<int:id_user>/<int:id_education>', methods=['PUT'])
def update_education(id_user, id_education):
    resume = Resume.query.filter_by(id_user=id_user).first()
    if not resume:
        return jsonify({"msg": "Resume for user not found"}), 404

    data = request.get_json()

    # Проверка, что все необходимые поля переданы
    required_fields = ['university', 'degree', 'direction', 'group', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    # Находим запись об образовании для обновления
    education = Education.query.filter_by(id_education=id_education).first()
    if not education:
        return jsonify({"msg": "Education not found"}), 404

    # Обновляем поля на основе переданных данных
    education.id_university = int(data['university'])
    education.id_degree = int(data['degree'])
    education.id_direction = int(data['direction'])
    education.group_number = int(data['group'])

    try:
        education.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        education.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400

    try:
        db.session.commit()
        return jsonify({"msg": "Education updated successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to update education: {str(e)}"}), 500


@modal_api.route('/api/works/<int:id_resume>', methods=['GET'])
@jwt_required()  # Requires JWT for authentication
def get_works_by_resume(id_resume):
    current_user_id = get_jwt_identity()

    # Check if the resume belongs to the current user
    resume = Resume.query.filter_by(id_resume=id_resume, id_user=current_user_id).first()
    if not resume:
        return jsonify({"msg": "Access denied or resume not found"}), 403

    works = Work.query.filter_by(id_resume=id_resume).all()
    work_list = []

    for work in works:
        organization_names = [org.organization_name for org in work.organizations]

        work_data = {
            'id_work': work.id_work,
            'organizations': organization_names,
            'position': work.position,
            'start_date': work.start_date.strftime('%Y-%m-%d') if work.start_date else None,
            'end_date': work.end_date.strftime('%Y-%m-%d') if work.end_date else None,
        }
        work_list.append(work_data)

    return jsonify(work_list), 200

@modal_api.route('/api/works/<int:id_user>/<int:id_work>', methods=['GET'])
@jwt_required()  # Requires JWT for authentication
def get_work_detail(id_user, id_work):
    current_user_id = get_jwt_identity()

    # Verify that the requested user matches the authenticated user
    if current_user_id != id_user:
        return jsonify({"msg": "Access denied"}), 403

    work = Work.query.filter_by(id_work=id_work).join(Resume).filter(Resume.id_user == id_user).first()
    if not work:
        return jsonify({"msg": "Work not found"}), 404

    organization_names = [org.organization_name for org in work.organizations]

    work_data = {
        'id_work': work.id_work,
        'organizations': organization_names,
        'position': work.position,
        'start_date': work.start_date.strftime('%Y-%m-%d') if work.start_date else None,
        'end_date': work.end_date.strftime('%Y-%m-%d') if work.end_date else None,
        "responsibilities": work.responsibilities
    }

    return jsonify(work_data), 200

@modal_api.route('/api/works/<int:id_user>', methods=['POST'])
def add_work(id_user):
    resume = Resume.query.filter_by(id_user=id_user).first()
    if not resume:
        return jsonify({"msg": "Resume for user not found"}), 404

    data = request.get_json()

    # Check that all required fields are provided
    required_fields = ['organization', 'position', 'start_date', 'end_date', 'responsibilities']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    try:
        new_work = Work(
            id_resume=resume.id_resume,
            position=data['position'],
            start_date=datetime.strptime(data['start_date'], '%Y-%m-%d'),
            end_date=datetime.strptime(data['end_date'], '%Y-%m-%d'),
            responsibilities=data['responsibilities']
        )

        db.session.add(new_work)
        db.session.flush()  # Get the new work ID before committing

        # Add the organization relationships
        organization_ids = data.get('organization_ids', [])
        for org_id in organization_ids:
            work_org = WorkOrganization(id_work=new_work.id_work, id_organization=org_id)
            db.session.add(work_org)

        db.session.commit()
        return jsonify({"msg": "Work added successfully", "id_work": new_work.id_work}), 201

    except ValueError as ve:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to add work: {str(e)}"}), 500

@modal_api.route('/api/works/<int:id_user>/<int:id_work>', methods=['PUT'])
def update_work(id_user, id_work):
    # Verify that the resume exists for the given user
    resume = Resume.query.filter_by(id_user=id_user).first()
    if not resume:
        return jsonify({"msg": "Resume for user not found"}), 404

    data = request.get_json()

    # Check that all required fields are provided
    required_fields = ['organization', 'position', 'start_date', 'end_date']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    # Find the work record to update
    work = Work.query.filter_by(id_work=id_work).filter(Work.id_resume == resume.id_resume).first()
    if not work:
        return jsonify({"msg": "Work experience not found"}), 404

    # Update fields based on provided data
    try:
        work.position = data['position']
        work.start_date = datetime.strptime(data['start_date'], '%Y-%m-%d')
        work.end_date = datetime.strptime(data['end_date'], '%Y-%m-%d')

        # Update the organizations (many-to-many relationship)
        if 'organization' in data:
            organization_ids = [int(org_id) for org_id in data['organization']]
            organizations = Organization.query.filter(Organization.id_organization.in_(organization_ids)).all()
            if not organizations:
                return jsonify({"msg": "One or more organizations not found"}), 404
            work.organizations = organizations

        db.session.commit()
        return jsonify({"msg": "Work experience updated successfully"}), 200
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to update work experience: {str(e)}"}), 500

@modal_api.route('/api/projects/<int:id_resume>', methods=['GET'])
def get_projects_by_resume(id_resume):
    projects = Projects.query.filter_by(id_resume=id_resume).all()
    project_list = []

    for project in projects:
        project_data = {
            'id_project': project.id_project,
            'project_name': project.project_name,
            'project_description': project.project_description,
            'project_link': project.project_link
        }
        project_list.append(project_data)

    return jsonify(project_list), 200

@modal_api.route('/api/projects/<int:id_resume>/<int:id_project>', methods=['GET'])
@jwt_required()
def get_project_detail(id_resume, id_project):
    # Ensure the user has permission to access the project
    project = Projects.query.filter_by(id_project=id_project, id_resume=id_resume).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    project_data = {
        'id_project': project.id_project,
        'project_name': project.project_name,
        'project_description': project.project_description,
        'project_link': project.project_link
    }

    return jsonify(project_data), 200
@modal_api.route('/api/project/<int:id_resume>', methods=['POST'])
def add_project(id_resume):
    data = request.get_json()

    required_fields = ['project_name', 'project_description', 'project_link']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    try:
        new_project = Projects(
            id_resume=id_resume,
            project_name=data['project_name'],
            project_description=data['project_description'],
            project_link=data['project_link']
        )

        db.session.add(new_project)
        db.session.commit()
        return jsonify({"msg": "Project added successfully", "id_project": new_project.id_project}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to add project: {str(e)}"}), 500

@modal_api.route('/api/projects/<int:id_user>/<int:id_project>', methods=['PUT'])
def update_project(id_user, id_project):
    # Verify that the resume exists for the given user
    resume = Resume.query.filter_by(id_user=id_user).first()
    if not resume:
        return jsonify({"msg": "Resume for user not found"}), 404

    data = request.get_json()

    # Check that all required fields are provided
    required_fields = ['project_name', 'project_description', 'project_link']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    # Find the project record to update
    project = Projects.query.filter_by(id_project=id_project, id_resume=resume.id_resume).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    # Update fields based on provided data
    try:
        project.project_name = data['project_name']
        project.project_description = data['project_description']
        project.project_link = data['project_link']

        db.session.commit()
        return jsonify({"msg": "Project updated successfully"}), 200
    except ValueError:
        return jsonify({"msg": "Invalid date format. Use YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to update project: {str(e)}"}), 500