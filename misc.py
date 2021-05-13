import logging
from telegram_token import token
from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from aiogram.contrib.fsm_storage.memory import MemoryStorage

bot = Bot(token)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)
