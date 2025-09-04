import os
from datetime import datetime

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage


token = '8378857988:AAG2kk54BIQKORdjFFQUAi-xMbhJsxp5de0' 
bot = Bot(token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

TG_CLIENT_ID = [972771697, 526632252]
