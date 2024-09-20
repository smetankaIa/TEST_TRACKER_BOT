from bot import bot, pagination_state
from func.fetch import fetch_tasks
from func.get_message import get_task_NOT_clossed_message
from telebot import types

class HandleAllTasks:            
    @staticmethod
    def handle_all_tasks(message):
        """Обработчик для всех задач"""
        tasks = fetch_tasks()  # Получаем все задачи
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