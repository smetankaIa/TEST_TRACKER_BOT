import time
from app.bot import bot


if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(15)  # Ждем 15 секунд перед повторным запуском