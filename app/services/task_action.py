from app.bot import pagination_state, types, bot
from app.func.inline_func import get_tasks_message
from app.func.fetch import fetch_tasks, fetch_user_tasks
from app.handlers.star_handler import StartHandler
from app.handlers.task_handler import TaskHandler




class HandlerTaskActions:            
    def handle_task_actions(message):
        user_id = message.from_user.id
        if message.text == "📑 Все задачи":
            tasks = fetch_user_tasks(user_id)
            if tasks:
                # Сохраняем задачи и текущую страницу для пользователя
                pagination_state[message.chat.id] = {
                    'tasks': tasks,
                    'page': 0
                }
                page = 0
                mes, keyboard = get_tasks_message(tasks, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню задач")
                markup.add(back)
                bot.send_message(message.chat.id, text="Нет доступных задач.", reply_markup=markup)

        elif message.text == "📄 Мои задачи (поиск по исполнителю)":
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            back = types.KeyboardButton("↪️ Вернуться в меню задач")
            markup.add(back)
            bot.send_message(message.chat.id, text="Напишите имя исполнителя для поиска задач", reply_markup=markup)

        elif message.text == "↪️ Вернуться в главное меню":
            StartHandler.start(message)

        elif message.text == "↪️ Вернуться в меню задач":
            TaskHandler.task_menu(message)

        else:
            user_full_name = message.text.strip().lower()
            tasks = fetch_tasks()
            user_tasks = [task for task in tasks if task.get('assignee', {}).get('display', '').lower() == user_full_name]
            if user_tasks:
                # Сохраняем задачи и текущую страницу для пользователя
                pagination_state[message.chat.id] = {
                    'tasks': user_tasks,
                    'page': 0
                }
                page = 0
                mes, keyboard = get_tasks_message(user_tasks, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню задач")
                markup.add(back)
                bot.send_message(message.chat.id, text="Задачи не найдены.", reply_markup=markup)
