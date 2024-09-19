import os
from dotenv import load_dotenv
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

# Импортируем и подключаем обработчики
from handlers.star_handler import StartHandler
from handlers.task_handler import TaskHandler
from handlers.project_handler import ProjectHandler
from handlers.text_handler import TextHandler
from func.callback import PaginationProject, PagintationTask, PaginationClosedTask


paginationClosedTask = PaginationClosedTask()
paginationTask = PagintationTask()
paginationProj = PaginationProject()
text_handler = TextHandler()
start_handler = StartHandler()
task_handler = TaskHandler()
project_handler = ProjectHandler()
