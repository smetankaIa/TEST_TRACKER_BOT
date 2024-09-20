from handlers.star_handler import StartHandler
from handlers.task_handler import TaskHandler
from func.get_message import get_personal_tasks_message
from func.fetch import fetch_user_tasks 
from bot import pagination_state, types, bot, user_state

class PersonHandler:    
    def handle_task_actions(message):
        user_id = message.from_user.id
        if message.text == "📄 Мои задачи (поиск по исполнителю)":
                tasks = fetch_user_tasks(user_id)  # Получаем личные задачи пользователя
                user_state_entry = user_state.get(message.chat.id, {})
                saved_name = user_state_entry.get('name', None)
                if tasks:
                    # Сохраняем личные задачи и текущую страницу для пользователя
                    pagination_state[message.chat.id] = {
                        'personal_tasks': tasks,  # Отдельно сохраняем личные задачи
                        'page': 0
                    }
                    page = 0
                    mes, keyboard = get_personal_tasks_message(tasks, page)
                    bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    back = types.KeyboardButton("↪️ Вернуться в меню задач")
                    markup.add(back)
                    bot.send_message(message.chat.id, text="Нет личных задач.", reply_markup=markup)
        elif message.text == "↪️ Вернуться в главное меню":
                StartHandler.start(message)

        elif message.text == "↪️ Вернуться в меню задач":
                TaskHandler.task_menu(message)

        else:
            bot.send_message(message.chat.id, text="Команда не распознана. Пожалуйста, выберите действие из меню.")
            