import asyncio

from aiogram import Bot, Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from stuff.settings import API_TOKEN

storage = MemoryStorage()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN, parse_mode='html', loop=loop)
dp = Dispatcher(bot, storage=storage, loop=loop)

del storage
