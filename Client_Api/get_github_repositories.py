from flask import Blueprint, jsonify, request
import requests
from langchain_community.chat_models import GigaChat
from langchain_core.messages import SystemMessage

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
