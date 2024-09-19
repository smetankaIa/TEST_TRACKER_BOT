from bot import pagination_state, types, bot, user_state
from func.get_message import get_tasks_message, get_closed_tasks_message, get_task_NOT_clossed_message
from func.fetch import fetch_tasks, fetch_user_tasks
from handlers.star_handler import StartHandler
from handlers.task_handler import TaskHandler

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
                mes, keyboard = get_task_NOT_clossed_message(tasks, page)
                bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                back = types.KeyboardButton("↪️ Вернуться в меню задач")
                markup.add(back)
                bot.send_message(message.chat.id, text="Нет доступных задач.", reply_markup=markup)

        elif message.text == "Закрытые задачи":
                tasks = fetch_user_tasks(user_id)
                
                if tasks: 
                    pagination_state[message.chat.id] = {
                        'tasks': tasks,
                        'page' : 0
                    }
                    page = 0
                    mes, keyboard = get_closed_tasks_message(tasks, page)
                    bot.send_message(message.chat.id, text=mes, reply_markup=keyboard)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    back = types.KeyboardButton("↪️ Вернуться в меню задач")
                    markup.add(back)
                    bot.send_message(message.chat.id, text=f"Закрытых задач нет", reply_markup=markup)
                return
        elif message.text == "📄 Мои задачи (поиск по исполнителю)":
            user_state_entry = user_state.get(message.chat.id, {})
            saved_name = user_state_entry.get('name', None)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            back = types.KeyboardButton("↪️ Вернуться в меню задач")
            if saved_name:
                btn_saved_name = types.KeyboardButton(saved_name)
                btn_other = types.KeyboardButton("Другое")
                markup.add(btn_saved_name, btn_other)
            else:
                markup.add(back)
                bot.send_message(message.chat.id, text="Напишите имя исполнителя для поиска задач", reply_markup=markup)
                user_state_entry['state'] = 'waiting_for_executor_name'
                user_state[message.chat.id] = user_state_entry
                return
            markup.add(back)
            bot.send_message(message.chat.id, text="Выберите имя исполнителя или нажмите 'Другое':", reply_markup=markup)
            user_state_entry['state'] = 'selecting_executor_name'
            user_state[message.chat.id] = user_state_entry

        elif message.text == "↪️ Вернуться в главное меню":
            StartHandler.start(message)

        elif message.text == "↪️ Вернуться в меню задач":
            TaskHandler.task_menu(message)

        else:
            bot.send_message(message.chat.id, text="Команда не распознана. Пожалуйста, выберите действие из меню.")
