from flask import Blueprint, jsonify, request
import requests
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage

from Client_Api.extensions import db
from Models import Skills, Projects, ProjectSkills

# Инициализация GigaChat
giga = GigaChat(
    credentials="N2Q2MjFiYmUtN2IwNy00ODNhLTk3MGQtOTUyNmQyYjAyNTY1Ojg4MzBkMmIwLThlMzItNDQyNi1hYzI1LTQ0ZmI0MWVkYmI2Mg==",
    scope="GIGACHAT_API_PERS", verify_ssl_certs=False, streaming=True
)


# Вспомогательные функции для работы с GitHub API
def get_username_from_url(url: str) -> str:
    return url.strip().split('/')[-1]


def get_repositories(username: str, token: str = "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"):
    url = f"https://api.github.com/users/{username}/repos"
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        return None


def get_languages(repo_full_name: str, token: str = "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"):
    url = f"https://api.github.com/repos/{repo_full_name}/languages"
    headers = {}
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return list(response.json().keys())
    else:
        return []


def get_topics(repo_full_name: str, token: str = "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"):
    url = f"https://api.github.com/repos/{repo_full_name}/topics"
    headers = {
        'Accept': 'application/vnd.github.mercy-preview+json'  # Для получения тем репозитория
    }
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('names', [])  # Получаем список тем из ответа
    else:
        return []


def get_readme_content(repo_full_name: str, token: str = "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"):
    """Функция для получения содержимого README.md, если он существует"""
    url = f"https://api.github.com/repos/{repo_full_name}/readme"
    headers = {
        'Accept': 'application/vnd.github.VERSION.raw'
    }
    if token:
        headers['Authorization'] = f"token {token}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text  # Возвращаем содержимое README.md в виде текста
    else:
        return "README.md отсутствует"  # Если README.md нет, возвращаем сообщение


# Генерация описания с помощью нейросети
def generate_description(repo_data):
    # Сообщение должно быть в виде списка с метаданными

    messages = [
        SystemMessage(
            content=f"Сгенерируй описание репозитория по данным на 2 предложения на русском языке: '{repo_data['name']}'. Используемые языки: {', '.join(repo_data['languages'])}. Используемые топики: {', '.join(repo_data['topics']) if repo_data['topics'] else None}. ReadMe.md: {', '.join(repo_data['readme_content']) if repo_data['readme_content'] else None}"
        )
    ]

    # Вызов модели с сообщением
    res = giga(messages)

    # Возвращаем сгенерированный текст
    return res.content


# Маршрут для получения информации о репозиториях
github_api = Blueprint('github_api', __name__)


@github_api.route('/repos', methods=['GET'])
def get_repos():
    github_url = request.args.get('github_url')
    token = request.args.get('token', "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")

    if not github_url:
        return jsonify({"error": "GitHub URL обязателен"}), 400

    username = get_username_from_url(github_url)
    repos = get_repositories(username, token)

    if repos is None:
        return jsonify({"error": "Не удалось получить репозитории"}), 500

    repo_info_list = []
    for repo in repos:
        repo_name = repo['name']
        repo_description = repo['description'] or "Описание отсутствует"
        repo_languages = get_languages(repo['full_name'], token)
        repo_topics = get_topics(repo['full_name'], token)
        repo_readme_content = get_readme_content(repo['full_name'], token)

        repo_data = {
            "name": repo_name,
            "description": repo_description,
            "languages": repo_languages,
            "topics": repo_topics,
            "readme_content": repo_readme_content  # Добавляем содержимое README.md
        }

        # Генерация описания с помощью нейросети
        generated_description = generate_description(repo_data)

        # Добавляем сгенерированное описание к данным о репозитории
        repo_info_list.append({
            "name": repo_name,
            "description": repo_description,
            "languages": repo_languages,
            "topics": repo_topics,
            "readme_content": repo_readme_content,
            "generated_description": generated_description  # Сгенерированное описание
        })

    return jsonify(repo_info_list), 200


# Вспомогательная функция для добавления навыков, чтобы избежать дублирования
def add_skill(skill_name):
    skill = Skills.query.filter_by(skill_name=skill_name).first()
    if skill is None:
        new_skill = Skills(skill_name=skill_name)
        db.session.add(new_skill)
        db.session.commit()
        return new_skill.id_skill
    return skill.id_skill


# Функция для добавления проектов в базу данных
def add_project(repo_data, resume_id):
    # Проверяем, существует ли проект с таким именем (по ссылке GitHub)
    existing_project = Projects.query.filter_by(project_link=repo_data['project_link']).first()

    if existing_project is None:
        # Добавляем новый проект
        new_project = Projects(
            id_resume=resume_id,
            project_name=repo_data['name'],
            project_description=repo_data['description'],
            project_link=repo_data['project_link']
        )
        db.session.add(new_project)
        db.session.commit()

        # Добавляем навыки (языки программирования и топики) к проекту
        for skill_name in repo_data['languages'] + repo_data['topics']:
            skill_id = add_skill(skill_name)
            # Добавляем связь проекта с навыком
            project_skill = ProjectSkills(id_project=new_project.id_project, id_skill=skill_id)
            db.session.add(project_skill)

        db.session.commit()
        return new_project
    return existing_project


# Маршрут для получения репозиториев и добавления их как проекты в базу данных
@github_api.route('/add_repos', methods=['GET'])
def post_repos():
    github_url = request.args.get('github_url')
    resume_id = request.args.get('resume_id')
    token = request.args.get('token', "your_default_token")

    if not github_url or not resume_id:
        return jsonify({"error": "GitHub URL и resume_id обязательны"}), 400

    username = get_username_from_url(github_url)
    repos = get_repositories(username, token)

    if repos is None:
        return jsonify({"error": "Не удалось получить репозитории"}), 500

    repo_info_list = []
    for repo in repos:
        repo_name = repo['name']
        repo_description = repo['description'] or "Описание отсутствует"
        repo_languages = get_languages(repo['full_name'], token)
        repo_topics = get_topics(repo['full_name'], token)
        repo_readme_content = get_readme_content(repo['full_name'], token)

        repo_data = {
            "name": repo_name,
            "description": repo_description,
            "languages": repo_languages,
            "topics": repo_topics,
            "readme_content": repo_readme_content,
            "project_link": repo['html_url']  # URL проекта на GitHub
        }

        # Генерация описания проекта с помощью нейросети
        generated_description = generate_description(repo_data)
        repo_data['generated_description'] = generated_description

        # Добавляем проект в базу данных
        project = add_project(repo_data, resume_id)

        # Добавляем информацию о проекте в список
        repo_info_list.append({
            "name": project.project_name,
            "description": project.project_description,
            "languages": repo_languages,
            "topics": repo_topics,
            "readme_content": repo_readme_content,
            "project_link": project.project_link,
            "generated_description": generated_description
        })

    return jsonify(repo_info_list), 200

