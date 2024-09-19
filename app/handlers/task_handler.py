from bot import bot, types, user_state
from roles import access_control, UserRole

class TaskHandler:        
    @bot.message_handler(func=lambda message: message.text == "Задачи")
    # @access_control([UserRole.DEVELOPER, UserRole.MANAGER, UserRole.ADMIN])
    def task_menu(message):
        user_state[message.chat.id]['state'] = 'tasks'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_all_tasks = types.KeyboardButton("📑 Все задачи")       
        btn_close_task = types.KeyboardButton("Закрытые задачи")
        btn_search_tasks = types.KeyboardButton("📄 Мои задачи (поиск по исполнителю)")
        back = types.KeyboardButton("↪️ Вернуться в главное меню")
        markup.add(btn_all_tasks,btn_close_task, btn_search_tasks, back)
        bot.send_message(message.chat.id, text="Вы в меню Задач.", reply_markup=markup)