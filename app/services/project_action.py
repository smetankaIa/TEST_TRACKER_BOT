from func.fetch import fetch_projects, fetch_tasks
from func.get_message import get_projects_message, get_tasks_message
from handlers.project_handler import ProjectHandler
from bot import pagination_state, bot, types, user_state
from handlers.star_handler import StartHandler



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
            if projects:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню проектов")
                # Создаем кнопки с названиями проектов
                project_buttons = [types.KeyboardButton(project['name']) for project in projects]
                # Добавляем кнопки проектов в клавиатуру по 2 в ряд
                for i in range(0, len(project_buttons), 2):
                    markup.add(*project_buttons[i:i+2])
                markup.add(back)
                bot.send_message(message.chat.id, text="Выберите проект для поиска задач:", reply_markup=markup)
                user_state[message.chat.id]['state'] = 'selecting_project_for_tasks'
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню проектов")
                markup.add(back)
                bot.send_message(message.chat.id, text="Нет доступных проектов.", reply_markup=markup)

        elif message.text == "📄 Мои задачи в проекте (поиск по проекту)":
            projects = fetch_projects()
            if projects:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню проектов")
                # Создаем кнопки с названиями проектов
                project_buttons = [types.KeyboardButton(project['name']) for project in projects]
                # Добавляем кнопки проектов в клавиатуру по 2 в ряд
                for i in range(0, len(project_buttons), 2):
                    markup.add(*project_buttons[i:i+2])
                markup.add(back)
                bot.send_message(message.chat.id, text="Выберите проект для поиска ваших задач:", reply_markup=markup)
                user_state[message.chat.id]['state'] = 'selecting_project_for_assigned_tasks'
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню проектов")
                markup.add(back)
                bot.send_message(message.chat.id, text="Нет доступных проектов.", reply_markup=markup)

        elif message.text == "↪️ Вернуться в главное меню":
            user_state[message.chat.id]['state'] = None
            StartHandler.start(message)

        elif message.text == "↪️ Вернуться в меню проектов":
            user_state[message.chat.id]['state'] = 'projects'
            ProjectHandler.project_menu(message)

        else:
            bot.send_message(message.chat.id, text="Команда не распознана. Пожалуйста, выберите действие из меню.")
