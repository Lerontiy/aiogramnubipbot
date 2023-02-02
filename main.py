import asyncio
import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

from aiogram.utils.executor import start_webhook
from aiogram import types

from create_bot import dp, bot
from stuff.settings import MESSAGES, WEBHOOK_PATH, WEBHOOK_URL, WEBAPP_HOST, WEBAPP_PORT
from stuff.database import db

# мінус 2 години в heroku logsd

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
        await message.answer(text=MESSAGES["HELP_MESS"], parse_mode='html')



async def on_startup(dp):
    await bot.set_webhook(WEBHOOK_URL) 



async def on_shutdown(dp):
    logging.warning('Shutting down..')

    await bot.delete_webhook()   


async def ggwp():
    asyncio.create_task(start_webhook(
                        dispatcher=dp,
                        webhook_path=WEBHOOK_PATH,
                        on_startup=on_startup,
                        on_shutdown=on_shutdown,
                        skip_updates=False,
                        host=WEBAPP_HOST,
                        port=int(os.environ.get("PORT", WEBAPP_PORT)),
                        ))

    
async def main():
    asyncio.create_task(ggwp())

    print("main")

    while True:
        await asyncio.sleep(10)
        print("main після 10 секунд")
  

if __name__ == '__main__':
    asyncio.run(main())
    
    #start_webhook(
    #            dispatcher=dp,
    #            webhook_path=WEBHOOK_PATH,
    #            on_startup=on_startup,
    #            on_shutdown=on_shutdown,
    #            skip_updates=False,
    #            host=WEBAPP_HOST,
    #            port=int(os.environ.get("PORT", WEBAPP_PORT)),
    #            )
