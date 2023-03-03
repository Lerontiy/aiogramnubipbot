import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from stuff.settings import API_TOKEN

storage = MemoryStorage()

loop = asyncio.new_event_loop()

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, loop=loop, parse_mode='html')
dp = Dispatcher(bot, storage=storage)

del storage
