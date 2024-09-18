from app.bot import types, parser


# Функция для формирования сообщения с проектами и Inline клавиатурой (если потребуется)
def get_projects_message(projects, page, projects_per_page=5):
    total_pages = (len(projects) - 1) // projects_per_page + 1
    start = page * projects_per_page
    end = start + projects_per_page
    current_projects = projects[start:end]

    mes = "\n".join([f"Проект: {project['name']}" for project in current_projects])

    # Формируем Inline клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    if page > 0:
        buttons.append(types.InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=f"projects_prev_{page - 1}"
        ))
    if end < len(projects):
        buttons.append(types.InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=f"projects_next_{page + 1}"
        ))
    if buttons:
        keyboard.add(*buttons)
    return mes, keyboard

def get_tasks_message(tasks, page, tasks_per_page=3):
    # Фильтруем задачи, исключая задачи со статусом "Закрыта"
    tasks = [task for task in tasks if task.get('status', {}).get('display', '').lower() != 'закрыта']

    total_pages = (len(tasks) - 1) // tasks_per_page + 1
    start = page * tasks_per_page
    end = start + tasks_per_page
    current_tasks = tasks[start:end]

    mes = "\n".join([
        f"ID: {task['id']}, \nНазвание: {task['summary']}, \n"
        f"Автор задачи: {task.get('createdBy', {}).get('display')}, \n"
        f"Проект: {task.get('project', {}).get('display')}, \n"
        f"Исполнитель: {task.get('assignee', {}).get('display', 'Не назначен')}, \n"
        f"Приоритет: 🔺 {task.get('priority', {}).get('display', 'Не назначен')}, \n"
        f"Дата создания: {parser.parse(task.get('createdAt')).date()}, \n"
        f"Дата дедлайна: {task.get('deadline', 'Не установлен')}, \n"
        f"Статус задачи: {task.get('status', {}).get('display')}\n\n"
        for task in current_tasks
    ])

    # Формируем Inline клавиатуру
    keyboard = types.InlineKeyboardMarkup()
    buttons = []
    if page > 0:
        buttons.append(types.InlineKeyboardButton(
            text="⬅️ Предыдущая",
            callback_data=f"tasks_prev_{page - 1}"
        ))
    if end < len(tasks):
        buttons.append(types.InlineKeyboardButton(
            text="Следующая ➡️",
            callback_data=f"tasks_next_{page + 1}"
        ))
    if buttons:
        keyboard.add(*buttons)
    return mes, keyboard