import json
from enum import Enum

# Определение ролей
class UserRole(Enum):
    USER = 'user'
    DEVELOPER = 'developer'
    MANAGER = 'manager'
    ADMIN = 'admin'

# Хранение ролей пользователей
user_roles = {}

def load_user_roles():
    global user_roles
    try:
        with open('user_roles.json', 'r') as f:
            data = json.load(f)
            user_roles = {int(k): UserRole(v) for k, v in data.items()}
    except FileNotFoundError:
        user_roles = {}

def save_user_roles():
    with open('user_roles.json', 'w') as f:
        data = {str(k): v.value for k, v in user_roles.items()}
        json.dump(data, f)

def set_user_role(user_id, role):
    user_roles[user_id] = role
    save_user_roles()

def get_user_role(user_id):
    return user_roles.get(user_id, UserRole.USER)

def access_control(allowed_roles):
    def decorator(func):
        def wrapper(message, *args, **kwargs):
            from mainK import bot  # Импортируем экземпляр бота
            user_id = message.from_user.id
            user_role = get_user_role(user_id)
            if user_role in allowed_roles:
                return func(message, *args, **kwargs)
            else:
                bot.reply_to(message, "У вас нет доступа к этой функции.")
        return wrapper
    return decorator