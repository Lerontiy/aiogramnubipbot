import logging
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

from aiogram.utils.executor import start_webhook
from aiogram import types

from create_bot import dp, bot
from stuff.settings import MESSAGES
from stuff.database import db


from handlers import handlers, callback, admin
async def on_startup():
    await bot.set_webhook("https://aiogramnubipbot.herokuapp.com/")

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


if __name__ == '__main__':
    #executor.start_polling(dp, skip_updates=True)
    #server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    start_webhook(
        dispatcher=dp,
        on_startup=on_startup,
        skip_updates=True,
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
    )