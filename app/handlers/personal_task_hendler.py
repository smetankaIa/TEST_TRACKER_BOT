from bot import bot, pagination_state, user_state
from func.get_message import get_personal_tasks_message
from telebot import types

class HandlerPersonalTaskActions:            
    @staticmethod
    def handle_personal_tasks(message):
        """Обработчик для личных задач"""
        user_state_entry = user_state.get(message.chat.id, {})
        saved_name = user_state_entry.get('name', None)
        
        # Клавиатура для выбора имени исполнителя
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