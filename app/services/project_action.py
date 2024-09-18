from app.func.fetch import fetch_projects, fetch_tasks
from app.func.get_message import get_projects_message, get_tasks_message
from app.handlers.project_handler import ProjectHandler
from app.bot import pagination_state, bot, types, user_state
from app.handlers.star_handler import StartHandler



# Обработка действий в меню проектов
class HandlerProjectActions:                
    def handle_project_actions(message):
        if message.text == "Все проекты":
            projects = fetch_projects()
            if projects:
                # Сохраняем проекты и текущую страницу для пользователя
                pagination_state[message.chat.id] = {
                    'projects': projects,
                    'page': 0
                }
                page = 0
                mes, keyboard = get_projects_message(projects, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню проектов")
                markup.add(back)
                bot.send_message(message.chat.id, text="Нет доступных проектов.", reply_markup=markup)

        elif message.text == "📄Задачи проекта (поиск по проекту)":
            projects = fetch_projects()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("↪️ Вернуться в меню проектов")
            project_buttons = [types.KeyboardButton(project['name']) for project in projects]
            for i in range(0, len(project_buttons), 2):
                    markup.add(*project_buttons[i:i+2])
            markup.add(back)
            if projects:
                mes = "\n".join([f"Проект: {project['name']}" for project in projects])
                bot.send_message(message.chat.id, text=f"Напишите название проекта для поиска задач\nСписок проектов:\n{mes}", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text="Нет доступных проектов.", reply_markup=markup)
            user_state[message.chat.id]['state'] = 'waiting_for_project_name_for_tasks'

        elif message.text == "📄 Мои задачи в проекте (поиск по проекту)":
            projects = fetch_projects()
            user_state_entry = user_state.get(message.chat.id, {})
            user_state_entry['state'] = 'waiting_for_project_name_for_assigned_tasks'
            user_state[message.chat.id] = user_state_entry
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("↪️ Вернуться в меню проектов")
            project_buttons = [types.KeyboardButton(project['name']) for project in projects]
            for i in range(0, len(project_buttons), 2):
                    markup.add(*project_buttons[i:i+2])
            markup.add(back)
            if projects:
                mes = "\n".join([f"Проект: {project['name']}" for project in projects])
                bot.send_message(message.chat.id, text=f"Выберите проект для поиска своих задач", reply_markup=markup)
            else:
                bot.send_message(message.chat.id, text="Нет доступных проектов.", reply_markup=markup)

        elif message.text == "↪️ Вернуться в главное меню":
            user_state[message.chat.id]['state'] = None
            StartHandler.start(message)

        elif message.text == "↪️ Вернуться в меню проектов":
            user_state[message.chat.id]['state'] = 'projects'
            ProjectHandler.project_menu(message)

        else:
            project_name = message.text.strip().lower()
            tasks = fetch_tasks()
            project_tasks = [
                task for task in tasks
                if task.get('project', {}).get('display', '').lower() == project_name
            ]
            if project_tasks:
                # Сохраняем задачи и текущую страницу для пользователя
                pagination_state[message.chat.id] = {
                    'tasks': project_tasks,
                    'page': 0
                }
                page = 0
                mes, keyboard = get_tasks_message(project_tasks, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, text=f"Задачи проекта '{project_name}' не найдены")
