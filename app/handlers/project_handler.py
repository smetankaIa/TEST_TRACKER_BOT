from bot import bot, user_state, types
from roles import access_control, UserRole


class ProjectHandler:        
    @bot.message_handler(func=lambda message: message.text == "Проекты")
    # @access_control([UserRole.DEVELOPER, UserRole.MANAGER, UserRole.ADMIN])
    def project_menu(message):
        user_state[message.chat.id]['state'] = 'projects'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn_all_projects = types.KeyboardButton("Все проекты")
        btn_search_tasks = types.KeyboardButton("📄Задачи проекта (поиск по проекту)")
        btn_search_tasks_in_projects = types.KeyboardButton("📄 Мои задачи в проекте (поиск по проекту)")
        back = types.KeyboardButton("↪️ Вернуться в главное меню")
        markup.add(btn_all_projects, btn_search_tasks, btn_search_tasks_in_projects, back)
        bot.send_message(message.chat.id, text="Вы в меню Проектов.", reply_markup=markup)