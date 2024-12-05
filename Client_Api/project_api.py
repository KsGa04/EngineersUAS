# ================= API для Проекты =================
import base64
from datetime import datetime

from flask import jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from langfuse.api import Project
from sqlalchemy import func, or_
from sqlalchemy.orm import joinedload, selectinload

from Client_Api.extensions import db
from Models import UserSocialNetwork, Education, Skills, University, Direction, Group, Degree, Organization, User, \
    Resume, ResumeSkills, Projects, WorkOrganization, ProjectSkills
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
    if not data or not data.get('skill_name'):
        return jsonify({"error": "skill_name is required"}), 400

    new_skill = Skills(skill_name=data['skill_name'])
    db.session.add(new_skill)
    db.session.commit()
    return jsonify({"message": "Навык добавлен", "id": new_skill.id_skill}), 201



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
    # Проверяем, существует ли запись в ResumeSkills
    resume_skill = ResumeSkills.query.get(id)
    if not resume_skill:
        return jsonify({"error": "Связь резюме и навыка не найдена"}), 404

    try:
        # Удаляем запись из ResumeSkills
        db.session.delete(resume_skill)
        db.session.commit()
        return jsonify({"message": "Навык успешно удален из резюме"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ошибка при удалении навыка из резюме: {str(e)}"}), 500

@modal_api.route('/api/resume_skills', methods=['POST'])
def add_resume_skill():
    try:
        data = request.get_json()
        id_resume = data.get('id_resume')
        id_skill = data.get('id_skill')

        # Проверка наличия данных
        if not id_resume or not id_skill:
            return jsonify({"error": "Отсутствуют необходимые данные."}), 400

        # Проверка на дублирование
        existing_skill = ResumeSkills.query.filter_by(id_resume=id_resume, id_skill=id_skill).first()
        if existing_skill:
            return jsonify({"error": "Этот навык уже добавлен."}), 400

        # Добавление нового навыка
        new_resume_skill = ResumeSkills(id_resume=id_resume, id_skill=id_skill)
        db.session.add(new_resume_skill)
        db.session.commit()

        return jsonify({"message": "Навык успешно добавлен."}), 201
    except Exception as e:
        return jsonify({"error": f"Ошибка при добавлении навыка: {str(e)}"}), 500

@modal_api.route('/api/resume/<int:resume_id>/skills', methods=['GET'])
def get_resume_skills(resume_id):
    try:
        # Находим все записи в таблице ResumeSkills, связанные с данным резюме
        resume_skills = ResumeSkills.query.filter_by(id_resume=resume_id).all()

        # Если навыков нет, возвращаем пустой список
        if not resume_skills:
            return jsonify({"skills": []}), 200

        # Собираем данные о навыках
        skills = []
        for resume_skill in resume_skills:
            skill = Skills.query.get(resume_skill.id_skill)
            if skill:  # Если навык существует
                skills.append({
                    "id_resume_skill": resume_skill.id_resume_skills,
                    "id_skill": skill.id_skill,
                    "skill_name": skill.skill_name
                })

        return jsonify({"skills": skills}), 200
    except Exception as e:
        return jsonify({"error": f"Ошибка при получении навыков: {str(e)}"}), 500




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
    university_list = [{"id": u.id_university, "name": u.short_name} for u in universities]
    return jsonify(university_list)

@modal_api.route('/api/skills', methods=['GET'])
def get_skills():
    universities = Skills.query.all()
    university_list = [{"id": u.id_skill, "name": u.skill_name} for u in universities]
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
    # Получение параметров запроса
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 10))
    search_query = request.args.get('search', '').lower()
    region_filter = request.args.get('region', '').lower()
    university_filter = request.args.get('university', '').lower()
    direction_filter = request.args.get('direction', '').lower()
    skill_filter = request.args.get('skill', '').lower()

    # Базовый запрос
    query = db.session.query(User).filter(User.role_id == 1)

    # Поиск
    if search_query:
        query = query.filter(
            db.or_(
                db.func.lower(User.first_name).like(f"%{search_query}%"),
                db.func.lower(User.last_name).like(f"%{search_query}%"),
                db.func.lower(User.middle_name).like(f"%{search_query}%")
            )
        )

    # Фильтр по региону
    if region_filter:
        query = query.filter(db.func.lower(User.address).like(f"%{region_filter}%"))

    # Фильтры по образованию и навыкам
    if university_filter or direction_filter or skill_filter:
        subquery = db.session.query(Resume.id_user).distinct()
        if university_filter:
            subquery = subquery.join(Education).join(University).filter(
                db.func.lower(University.short_name).like(f"%{university_filter}%")
            )
        if direction_filter:
            subquery = subquery.join(Education).join(Direction).filter(
                db.func.lower(Direction.direction_name).like(f"%{direction_filter}%")
            )
        if skill_filter:
            subquery = subquery.join(ResumeSkills, Resume.id_resume == ResumeSkills.id_resume).join(
                Skills, ResumeSkills.id_skill == Skills.id_skill
            ).filter(db.func.lower(Skills.skill_name).like(f"%{skill_filter}%"))
        user_ids = [row[0] for row in subquery.all()]
        query = query.filter(User.id_user.in_(user_ids))

    # Предзагрузка данных
    candidates = query.options(
        selectinload(User.resumes)
        .selectinload(Resume.educations),
        selectinload(User.resumes)
        .selectinload(Resume.projects),
    ).offset((page - 1) * limit).limit(limit).all()

    # Сериализация данных
    result = []
    for user in candidates:
        profile_photo_data = (
            f"data:image/jpeg;base64,{base64.b64encode(user.profile_photo).decode('utf-8')}" if user.profile_photo else None
        )

        serialized_resumes = []
        for resume in user.resumes:
            educations = [
                {
                    'id_education': edu.id_education,
                    'university_name': edu.university.full_name if edu.university else None,
                    'direction_name': edu.direction.direction_name if edu.direction else None,
                    'city': edu.university.location if edu.university else None,
                }
                for edu in Education.query.filter_by(id_resume=resume.id_resume).all()
            ]

            skills = [
                {
                    'id_skill': skill.id_skill,
                    'skill_name': skill.skill_name,
                }
                for skill in db.session.query(Skills).join(ResumeSkills).filter(ResumeSkills.id_resume == resume.id_resume).all()
            ]

            serialized_resumes.append({
                'id_resume': resume.id_resume,
                'about_me': resume.about_me,
                'id_pattern': resume.id_pattern,
                'educations': educations,
                'skills': skills,
            })

        result.append({
            'id_user': user.id_user,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'middle_name': user.middle_name,
            'email': user.email,
            'phone': user.phone,
            'birth_date': user.birth_date.strftime('%Y-%m-%d') if user.birth_date else None,
            'address': user.address,
            'profile_photo': profile_photo_data,
            'resumes': serialized_resumes,
        })

    return jsonify({
        'candidates': result,
        'total_pages': (query.count() + limit - 1) // limit,
        'current_page': page,
        'total_count': query.count(),
    })


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
    current_user_id = int(get_jwt_identity())

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
    current_user_id = int(get_jwt_identity())

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
    required_fields = ['university', 'degree', 'direction', 'group', 'start_date', 'end_date', 'completed']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    try:
        start_year = data['start_date'][:4]  # Take only the first 4 characters
        end_year = data['end_date'][:4]
        new_education = Education(
            id_resume=resume.id_resume,
            id_university=int(data['university']),
            id_degree=int(data['degree']),
            id_direction=int(data['direction']),
            group_number=int(data['group']),
            start_date=datetime.strptime(start_year, '%Y'),
            end_date=datetime.strptime(end_year, '%Y'),
            status=data['completed']
        )

        db.session.add(new_education)
        db.session.commit()
        return jsonify({"msg": "Образование успешно добавлено", "id_education": new_education.id_education}), 201

    except ValueError as ve:
        return jsonify({"msg": "Неправильный формат. Use YYYY-MM-DD."}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Ошибка добавления образования: {str(e)}"}), 500


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
        start_year = data['start_date'][:4]  # Take only the first 4 characters
        end_year = data['end_date'][:4]
        education.start_date = datetime.strptime(start_year, '%Y')
        education.end_date = datetime.strptime(end_year, '%Y')
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
    current_user_id = int(get_jwt_identity())

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
    current_user_id = int(get_jwt_identity())

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
        start_year = data['start_date'][:4]  # Take only the first 4 characters
        end_year = data['end_date'][:4]
        new_work = Work(
            id_resume=resume.id_resume,
            position=data['position'],
            start_date=datetime.strptime(start_year, '%Y'),
            end_date=datetime.strptime(end_year, '%Y'),
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
        start_year = data['start_date'][:4]  # Take only the first 4 characters
        end_year = data['end_date'][:4]
        work.start_date = datetime.strptime(start_year, '%Y')
        work.end_date = datetime.strptime(end_year, '%Y')

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
    skills = db.session.query(Skills).join(ProjectSkills).filter(ProjectSkills.id_project == id_project).all()
    skill_list = [{"id_skill": skill.id_skill, "skill_name": skill.skill_name} for skill in skills]
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    project_data = {
        'id_project': project.id_project,
        'project_name': project.project_name,
        'project_description': project.project_description,
        'project_link': project.project_link,
        'skill': skill_list
    }

    return jsonify(project_data), 200
@modal_api.route('/api/project/<int:id_resume>', methods=['POST'])
def add_project(id_resume):
    data = request.get_json()

    # Ensure required fields are provided
    required_fields = ['project_name', 'project_description', 'project_link', 'skills']
    for field in required_fields:
        if field not in data:
            return jsonify({"msg": f"'{field}' is required in the request data"}), 400

    try:
        # Create a new project instance
        new_project = Projects(
            id_resume=id_resume,
            project_name=data['project_name'],
            project_description=data['project_description'],
            project_link=data['project_link']
        )

        # Add the new project to the session to get its ID
        db.session.add(new_project)
        db.session.flush()  # Use flush to get the project ID before commit

        # Associate skills with the project using the ProjectsSkills table
        skill_ids = data.get("skills", [])
        for skill_id in skill_ids:
            project_skill = ProjectSkills(id_project=new_project.id_project, id_skill=skill_id)
            db.session.add(project_skill)

        # Commit the transaction
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
    
@modal_api.route('/api/projects/<int:project_id>/skills', methods=['POST'])
def add_skill_to_project(project_id):
    """Добавление навыка в проект."""
    data = request.get_json()

    # Проверяем наличие id_skill в запросе
    id_skill = data.get('id_skill')
    if not id_skill:
        return jsonify({"msg": "'id_skill' is required in the request data"}), 400

    # Проверяем, существует ли проект
    project = Projects.query.filter_by(id_project=project_id).first()
    if not project:
        return jsonify({"msg": "Project not found"}), 404

    # Проверяем, существует ли навык
    skill = Skills.query.filter_by(id_skill=id_skill).first()
    if not skill:
        return jsonify({"msg": "Skill not found"}), 404

    # Проверяем, не добавлен ли уже этот навык в проект
    existing_entry = ProjectSkills.query.filter_by(id_project=project_id, id_skill=id_skill).first()
    if existing_entry:
        return jsonify({"msg": "Skill is already added to the project"}), 400

    # Добавляем навык в проект
    try:
        new_skill = ProjectSkills(id_project=project_id, id_skill=id_skill)
        db.session.add(new_skill)
        db.session.commit()
        return jsonify({"msg": "Skill added to the project successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to add skill to project: {str(e)}"}), 500

@modal_api.route('/api/projects/<int:project_id>/skills/<int:skill_id>', methods=['DELETE'])
def remove_skill_from_project(project_id, skill_id):
    """Удаление навыка из проекта."""
    # Проверяем, существует ли запись в project_skills
    entry = ProjectSkills.query.filter_by(id_project=project_id, id_skill=skill_id).first()
    if not entry:
        return jsonify({"msg": "Skill not found in the project"}), 404

    # Удаляем навык из проекта
    try:
        db.session.delete(entry)
        db.session.commit()
        return jsonify({"msg": "Skill removed from the project successfully"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"msg": f"Failed to remove skill from project: {str(e)}"}), 500


@modal_api.route('/api/getall/<int:id_user>', methods=['get'])
def get_all(id_user):
    id_resume = Resume.query.filter_by(id_user=id_user).first().id_resume

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

    response = {
        'projects': project_list,
        'works': work_list,
        'educations': education_list,
    }

    return jsonify(response), 200
