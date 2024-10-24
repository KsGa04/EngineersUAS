from flask import Blueprint, jsonify, request
import requests
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage

giga = GigaChat(
    credentials="N2Q2MjFiYmUtN2IwNy00ODNhLTk3MGQtOTUyNmQyYjAyNTY1Ojg4MzBkMmIwLThlMzItNDQyNi1hYzI1LTQ0ZmI0MWVkYmI2Mg==",
    scope="GIGACHAT_API_PERS", verify_ssl_certs=False, streaming=True
)

def get_username_from_url(url: str) -> str:
    return url.strip().split('/')[-2]

def get_gitlab_repositories(username: str, token: str = "glpat-pc934YjiCQRV6F2As7tu"):
    url = f"https://gitlab.com/api/v4/users/{username}/projects"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    print(f'{response=}')
    if response.status_code == 200:
        return response.json()
    else:
        return None

def get_gitlab_languages(repo_id: int, token: str = "glpat-pc934YjiCQRV6F2As7tu"):
    url = f"https://gitlab.com/api/v4/projects/{repo_id}/languages"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return list(response.json().keys())
    else:
        return []

def get_gitlab_topics(repo_id: int, token: str = "glpat-pc934YjiCQRV6F2As7tu"):
    url = f"https://gitlab.com/api/v4/projects/{repo_id}/topics"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get('topics', [])
    else:
        return []

def get_gitlab_readme_content(repo_id: int, token: str = "glpat-pc934YjiCQRV6F2As7tu"):
    """Функция для получения содержимого README.md, если он существует"""
    url = f"https://gitlab.com/api/v4/projects/{repo_id}/repository/files/README.md/raw?ref=master"
    headers = {
        'Authorization': f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.text
    else:
        return "README.md отсутствует"

def generate_description(repo_data):
    messages = [
        SystemMessage(
            content=f"Сгенерируй описание репозитория по данным на 2 предложения на русском языке: '{repo_data['name']}'. Используемые языки: {', '.join(repo_data['languages'])}. Используемые топики: {', '.join(repo_data['topics']) if repo_data['topics'] else None}. ReadMe.md: {', '.join(repo_data['readme_content']) if repo_data['readme_content'] else None}"
        )
    ]
    res = giga(messages)
    return res.content

gitlab_api = Blueprint('gitlab_api', __name__)

@gitlab_api.route('/repos', methods=['GET'])
def get_gitlab_repos():
    gitlab_url = request.args.get('gitlab_url')
    token = request.args.get('token', "glpat-pc934YjiCQRV6F2As7tu")

    if not gitlab_url:
        return jsonify({"error": "GitLab URL обязателен"}), 400

    username = get_username_from_url(gitlab_url)
    repos = get_gitlab_repositories(username, token)

    if repos is None:
        return jsonify({"error": "Не удалось получить репозитории"}), 500

    repo_info_list = []
    for repo in repos:
        repo_id = repo['id']
        repo_name = repo['name']
        repo_description = repo['description'] or "Описание отсутствует"
        repo_languages = get_gitlab_languages(repo_id, token)
        repo_topics = get_gitlab_topics(repo_id, token)
        repo_readme_content = get_gitlab_readme_content(repo_id, token)

        repo_data = {
            "name": repo_name,
            "description": repo_description,
            "languages": repo_languages,
            "topics": repo_topics,
            "readme_content": repo_readme_content
        }

        generated_description = generate_description(repo_data)

        repo_info_list.append({
            "name": repo_name,
            "description": repo_description,
            "languages": repo_languages,
            "topics": repo_topics,
            "readme_content": repo_readme_content,
            "generated_description": generated_description
        })

    return jsonify(repo_info_list), 200
