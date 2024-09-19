from handlers.project_handler import ProjectHandler
from bot import bot, user_state, types, pagination_state
from handlers.star_handler import StartHandler
from func.fetch import fetch_tasks
from func.get_message import get_tasks_message, get_task_NOT_clossed_message, get_personal_tasks_message
from services.project_action import HandlerProjectActions
from services.task_action import HandlerTaskActions


class TextHandler:        
    @bot.message_handler(func=lambda message: True)
    def handle_text(message):
        user_state_entry = user_state.get(message.chat.id, {'state': None})
        user_state[message.chat.id] = user_state_entry

        # Обработка возврата в главное меню
        if message.text == "↪️ Вернуться в главное меню":
            user_state_entry['state'] = None
            StartHandler.start(message)
            return

        state = user_state_entry.get('state', None)

        if state == 'asking_for_name':
            # Сохраняем имя пользователя
            user_state_entry['name'] = message.text.strip()
            user_state_entry['state'] = None
            user_state[message.chat.id] = user_state_entry
            # Отображаем главное меню
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_tasks = types.KeyboardButton("Задачи")
            btn_projects = types.KeyboardButton("Проекты")
            markup.add(btn_tasks, btn_projects)
            bot.send_message(message.chat.id, text="Спасибо! Ваше имя сохранено.\nГлавное меню", reply_markup=markup)
            return

        elif state == 'selecting_executor_name':
            if message.text == "Другое":
                user_state_entry['state'] = 'waiting_for_executor_name'
                bot.send_message(message.chat.id, text="Напишите имя исполнителя для поиска задач")
                return
            else:
                executor_name = message.text.strip().lower()
                tasks = fetch_tasks()
                user_tasks = [task for task in tasks if task.get('assignee', {}).get('display', '').lower() == executor_name]
                if user_tasks:
                    pagination_state[message.chat.id] = {
                        'tasks': user_tasks,
                        'page': 0
                    }
                    page = 0
                    mes, keyboard = get_personal_tasks_message(user_tasks, page)
                    bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    back = types.KeyboardButton("↪️ Вернуться в меню задач")
                    markup.add(back)
                    bot.send_message(message.chat.id, text="Задачи не найдены.", reply_markup=markup)
                user_state_entry['state'] = 'tasks'
                user_state[message.chat.id] = user_state_entry
                return

        elif state == 'waiting_for_executor_name':
            executor_name = message.text.strip().lower()
            tasks = fetch_tasks()
            user_tasks = [task for task in tasks if task.get('assignee', {}).get('display', '').lower() == executor_name]
            if user_tasks:
                pagination_state[message.chat.id] = {
                    'tasks': user_tasks,
                    'page': 0
                }
                page = 0
                mes, keyboard = get_personal_tasks_message(user_tasks, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню задач")
                markup.add(back)
                bot.send_message(message.chat.id, text="Задачи не найдены.", reply_markup=markup)
            user_state_entry['state'] = 'tasks'
            user_state[message.chat.id] = user_state_entry
            return

        elif state == 'selecting_project_for_tasks':
            if message.text == "↪️ Вернуться в меню проектов":
                user_state_entry['state'] = 'projects'
                ProjectHandler.project_menu(message)
                return
            else:
                project_name = message.text.strip().lower()
                tasks = fetch_tasks()
                project_tasks = [
                    task for task in tasks
                    if task.get('project', {}).get('display', '').lower() == project_name
                ]
                if project_tasks:
                    pagination_state[message.chat.id] = {
                        'tasks': project_tasks,
                        'page': 0
                    }
                    page = 0
                    mes, keyboard = get_tasks_message(project_tasks, page)
                    bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, text=f"Задачи проекта '{project_name}' не найдены")
                user_state_entry['state'] = 'projects'
                return

        elif state == 'selecting_project_for_assigned_tasks':
            if message.text == "↪️ Вернуться в меню проектов":
                user_state_entry['state'] = 'projects'
                ProjectHandler.project_menu(message)
                return
            else:
                project_name = message.text.strip()
                user_state_entry['project_name'] = project_name
                user_state[message.chat.id] = user_state_entry

                # Предлагаем сохраненное имя и "Другое"
                saved_name = user_state_entry.get('name', None)
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню проектов")
                if saved_name:
                    btn_saved_name = types.KeyboardButton(saved_name)
                    btn_other = types.KeyboardButton("Другое")
                    markup.add(btn_saved_name, btn_other)
                    markup.add(back)
                    bot.send_message(message.chat.id, text="Выберите имя исполнителя или нажмите 'Другое':", reply_markup=markup)
                    user_state_entry['state'] = 'selecting_executor_name_in_project'
                    user_state[message.chat.id] = user_state_entry
                    return
                else:
                    markup.add(back)
                    bot.send_message(message.chat.id, text="Напишите имя исполнителя для поиска задач", reply_markup=markup)
                    user_state_entry['state'] = 'waiting_for_executor_name_in_project'
                    user_state[message.chat.id] = user_state_entry
                    return

        elif state == 'selecting_executor_name_in_project':
            if message.text == "Другое":
                user_state_entry['state'] = 'waiting_for_executor_name_in_project'
                bot.send_message(message.chat.id, text="Напишите имя исполнителя для поиска задач")
                return
            else:
                executor_name = message.text.strip().lower()
                project_name = user_state_entry.get('project_name', '').strip().lower()
                tasks = fetch_tasks()
                matching_tasks = [
                    task for task in tasks
                    if task.get('project', {}).get('display', '').lower() == project_name and
                    task.get('assignee', {}).get('display', '').lower() == executor_name
                ]
                if matching_tasks:
                    pagination_state[message.chat.id] = {
                        'tasks': matching_tasks,
                        'page': 0
                    }
                    page = 0
                    mes, keyboard = get_tasks_message(matching_tasks, page)
                    bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
                else:
                    bot.send_message(message.chat.id, text=f"Задачи для исполнителя '{executor_name}' в проекте '{project_name}' не найдены.")
                user_state_entry['state'] = 'projects'
                user_state[message.chat.id] = user_state_entry
                return

        elif state == 'waiting_for_executor_name_in_project':
            executor_name = message.text.strip().lower()
            project_name = user_state_entry.get('project_name', '').strip().lower()
            tasks = fetch_tasks()
            matching_tasks = [
                task for task in tasks
                if task.get('project', {}).get('display', '').lower() == project_name and
                task.get('assignee', {}).get('display', '').lower() == executor_name
            ]
            if matching_tasks:
                pagination_state[message.chat.id] = {
                    'tasks': matching_tasks,
                    'page': 0
                }
                page = 0
                mes, keyboard = get_tasks_message(matching_tasks, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                bot.send_message(message.chat.id, text=f"Задачи для исполнителя '{executor_name}' в проекте '{project_name}' не найдены.")
            user_state_entry['state'] = 'projects'
            user_state[message.chat.id] = user_state_entry
            return

        elif state == 'tasks':
            HandlerTaskActions.handle_task_actions(message)

        elif state == 'projects':
            HandlerProjectActions.handle_project_actions(message)
        else:
            bot.send_message(message.chat.id, text="Выберите действие из главного меню или напишите /start", reply_markup=types.ReplyKeyboardMarkup(resize_keyboard=True))
