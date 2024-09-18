from app.bot import bot, user_state, types

class StartHandler:
    @bot.message_handler(commands=['start'])
    def start(message):
        chat_id = message.chat.id
        user_state_entry = user_state.get(chat_id, {})
        if 'name' not in user_state_entry:
            user_state_entry['state'] = 'asking_for_name'
            user_state[chat_id] = user_state_entry
            bot.send_message(chat_id, text="Пожалуйста, введите ваше имя и фамилию:")
        else:
            user_state_entry['state'] = None
            user_state[chat_id] = user_state_entry
            # Отображаем главное меню
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            btn_tasks = types.KeyboardButton("Задачи")
            btn_projects = types.KeyboardButton("Проекты")
            btn_gpt = types.KeyboardButton("ChatGPT")
            markup.add(btn_tasks, btn_projects, btn_gpt)
            bot.send_message(chat_id, text="Главное меню", reply_markup=markup)
