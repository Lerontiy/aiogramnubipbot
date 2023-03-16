import asyncio
import logging
import os

import nest_asyncio
nest_asyncio.apply()

# Configure logging
logging.basicConfig(level=logging.INFO)

from aiogram.utils.executor import start_webhook, start_polling
from aiogram import types, executor

from create_bot import dp, bot, loop
from stuff.settings import WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT
from stuff.database import db
from stuff.my_requests import update_weekdays_html_timer, update_weekdays_html
from stuff.messages import MESSAGES
from stuff.functions import every

# мінус 2 години в heroku logs

from handlers import handlers, callback, admin
handlers.my_register_message_handler(dp)
callback.my_register_callback_query_handler(dp)
admin.my_admin_register_message_handler(dp)    


@dp.message_handler(chat_type=['private']) 
async def nothing(message: types.Message):
    db.check_user_in_db(message.from_id)

    if (db.user_is_admin(message.from_id)==True):
        await message.reply(message)
        await bot.send_photo(photo="AgACAgIAAxkBAAIKhmNe6GvJ_boVFKmcu60eQkx7cjgsAAITxDEbGbX5Si3n-2-h7v1lAQADAgADeAADKgQ", chat_id=message.from_user.id)
    else:
        await message.answer(text=MESSAGES['HELP_MESS'])


async def on_startup(dp):
    await db.recreate_sql()
    await bot.set_webhook(WEBHOOK_URL) 
    pass


async def on_shutdown(dp):
    await bot.delete_webhook()
    pass


if __name__ == '__main__':
    #asyncio.set_event_loop(loop)

    loop.create_task(every(1*5, update_weekdays_html))
    
    #executor.start_polling(
    #    dispatcher=dp,
    #    on_startup=on_startup,
    #    on_shutdown=on_shutdown,
    #    skip_updates=False,
    #    loop=loop,
    #    )
    
    executor.start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        skip_updates=False,
        host=WEBAPP_HOST,
        port=int(os.environ.get('PORT', WEBAPP_PORT)),
        loop=loop,
        )
    

    """ 
    змінити start_polling() на start_webhook() в main.py
    змінити дійсний API Token в settings.py 
    """
    
    
    

    
