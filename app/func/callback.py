from bot import bot, pagination_state, telebot
from func.get_message import get_projects_message, get_tasks_message, get_closed_tasks_message, get_task_NOT_clossed_message

# Обработка callback_query для пагинации задач
class PagintationTask:
    @bot.callback_query_handler(func=lambda call: call.data.startswith('tasks_'))
    def callback_tasks_pagination(call):
        chat_id = call.message.chat.id
        data = call.data

        if chat_id not in pagination_state or 'tasks' not in pagination_state[chat_id]:
            bot.answer_callback_query(call.id, "Срок действия этой сессии истек. Пожалуйста, запросите задачи снова.")
            return

        tasks = pagination_state[chat_id]['tasks']
        page = pagination_state[chat_id]['page']

        if 'next' in data:
            page += 1
        elif 'prev' in data and page > 0:
            page -= 1

        pagination_state[chat_id]['page'] = page

        mes, keyboard = get_task_NOT_clossed_message(tasks, page)
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=mes, reply_markup=keyboard)
        except telebot.apihelper.ApiTelegramException:
            # Если не удалось редактировать сообщение (например, слишком старое), отправляем новое
            bot.send_message(chat_id=chat_id, text=mes, reply_markup=keyboard)

        bot.answer_callback_query(call.id)
        
class PaginationProject:
# Обработка callback_query для пагинации проектов (если потребуется)
    @bot.callback_query_handler(func=lambda call: call.data.startswith('projects_'))
    def callback_projects_pagination(call):
        chat_id = call.message.chat.id
        data = call.data

        if chat_id not in pagination_state or 'projects' not in pagination_state[chat_id]:
            bot.answer_callback_query(call.id, "Срок действия этой сессии истек. Пожалуйста, запросите проекты снова.")
            return

        projects = pagination_state[chat_id]['projects']
        page = pagination_state[chat_id]['page']

        if 'next' in data:
            page += 1
        elif 'prev' in data and page > 0:
            page -= 1

        pagination_state[chat_id]['page'] = page

        mes, keyboard = get_projects_message(projects, page)
        try:
            bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=mes, reply_markup=keyboard)
        except telebot.apihelper.ApiTelegramException:
            # Если не удалось редактировать сообщение (например, слишком старое), отправляем новое
            bot.send_message(chat_id=chat_id, text=mes, reply_markup=keyboard)

        bot.answer_callback_query(call.id)

class PaginationClosedTask:
    @bot.callback_query_handler(func=lambda call: call.data.startswith('closed_tasks_'))
    def callback_closed_tasks_pagination(call):
        chat_id = call.message.chat.id
        data = call.data

        # Проверяем, существуют ли задачи для данного пользователя
        if chat_id not in pagination_state or 'tasks' not in pagination_state[chat_id]:
            bot.answer_callback_query(call.id, "Срок действия этой сессии истек. Пожалуйста, запросите задачи снова.")
            return

        tasks = pagination_state[chat_id]['tasks']  # Загружаем задачи из состояния пользователя
        page = pagination_state[chat_id]['page']

        # Обработка "следующая" страница
        if 'next' in data:
            if (page + 1) * 3 < len(tasks):  # Проверяем, есть ли задачи на следующей странице
                page += 1
            else:
                bot.answer_callback_query(call.id, "Больше задач нет.")
                return
        # Обработка "предыдущая" страница
        elif 'prev' in data and page > 0:
            page -= 1

        pagination_state[chat_id]['page'] = page

        # Получаем отфильтрованные закрытые задачи и отправляем пользователю
        mes, keyboard = get_closed_tasks_message(tasks, page)
        
        # Проверяем, что переменная mes не пустая
        if not mes.strip():
            bot.send_message(chat_id=chat_id, text="Закрытых задач больше нет.", reply_markup=keyboard)
        else:
            try:
                bot.edit_message_text(chat_id=chat_id, message_id=call.message.message_id, text=mes, reply_markup=keyboard)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(chat_id=chat_id, text=mes, reply_markup=keyboard)

        bot.answer_callback_query(call.id)