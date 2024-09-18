from bot import PROJECT_ID, YANDEX_TOKEN
import requests 
from roles import get_user_role, UserRole

# Получение всех задач из Yandex Tracker
def fetch_tasks():
    url = f'https://api.tracker.yandex.net/v2/issues?project={PROJECT_ID}'
    headers = {
        'Authorization': f'OAuth {YANDEX_TOKEN}',
        "X-Cloud-Org-ID": PROJECT_ID
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении задач: {e}")
        return []

# Получение всех проектов из Yandex Tracker
def fetch_projects():
    url = f'https://api.tracker.yandex.net/v2/projects?project={PROJECT_ID}'
    headers = {
        'Authorization': f'OAuth {YANDEX_TOKEN}',
        "X-Cloud-Org-ID": PROJECT_ID
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"Ошибка при получении проектов: {e}")
        return []
    
# Функция для получения задач пользователя с учетом его роли
def fetch_user_tasks(user_id):
    user_role = get_user_role(user_id)
    tasks = fetch_tasks()

    if user_role == UserRole.USER:
        # Возвращаем только задачи, назначенные на пользователя
        tasks = [task for task in tasks if task.get('assignee', {}).get('id') == user_id]
    elif user_role == UserRole.DEVELOPER:
        # Возвращаем задачи, связанные с разработчиком (можно уточнить критерии)
        # Здесь просто возвращаем все задачи
        tasks = tasks
    elif user_role in [UserRole.MANAGER, UserRole.ADMIN]:
        # Возвращаем все задачи
        tasks = tasks
    else:
        tasks = []
    return tasks    