import os
from dotenv import load_dotenv
from telebot import TeleBot
import telebot
from dateutil import parser
from telebot import types
from yandex_tracker_client import TrackerClient
from roles import load_user_roles

load_user_roles()
load_dotenv()
# Настройки бота и Yandex Tracker
TELEGRAM_TOKEN = os.getenv('TELEGRAM')
YANDEX_TOKEN = os.getenv('YANDEX')
PROJECT_ID = os.getenv('PROJECT')
# Инициализация бота и Yandex Tracker API
bot = telebot.TeleBot(TELEGRAM_TOKEN)
client = TrackerClient(token=YANDEX_TOKEN, org_id=PROJECT_ID)
# Переменные для отслеживания состояния пользователя и истории общения с ChatGPT
user_state = {}
user_conversations = {}  # Определяем переменную user_conversations

# Переменные для хранения состояния пагинации по пользователям
pagination_state = {}
client = TrackerClient(token=YANDEX_TOKEN, org_id=PROJECT_ID)

# Импортируем и подключаем обработчики
from app.handlers.star_handler import StartHandler
from app.handlers.task_handler import TaskHandler
from app.handlers.project_handler import ProjectHandler

start_handler = StartHandler()
task_handler = TaskHandler()
project_handler = ProjectHandler()
