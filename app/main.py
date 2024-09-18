import time
from bot import bot
from roles import load_user_roles

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
            load_user_roles()
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(15)  # Ждем 15 секунд перед повторным запуском