from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from create_bot import bot
from stuff.settings import FSM_ikm, MESSAGES
from stuff.database import db


# /admin
async def admin(message: types.Message):
    if (message.chat.id==int("-1001829277626")) and (message.from_user.id==int("706030949")):
        db.check_user_in_db(message.reply_to_message.from_user.id)
        db.change_acctype(message.reply_to_message.from_user.id, '1')
        
        await message.reply_to_message.reply(f"Ти успішно стаєш адміністратором!\nId: {message.reply_to_message.from_user.id}")
        await bot.send_message(message.reply_to_message.from_user.id, text="Ти успішно стаєш адміністратором!", reply_markup=FSM_ikm)


# /noadmin
async def noadmin(message: types.Message):
    if (message.chat.id==int("-1001829277626")) and (message.from_user.id==int("706030949")):
        db.check_user_in_db(message.reply_to_message.from_user.id)
        db.change_acctype(message.reply_to_message.from_user.id, '0')
        
        adm_ikm = ReplyKeyboardRemove()
        await message.reply_to_message.reply(f"Нажаль, ти більше не адміністратор!\nId: {message.reply_to_message.from_user.id}")
        await bot.send_message(message.reply_to_message.from_user.id, text="Нажаль, ти більше не адміністратор!", reply_markup=adm_ikm)


class Advertisment(StatesGroup):
    what_message = State()
    send_or_not = State()

#📢
# початок створення оголошення
async def advert(message: types.Message):
    if db.user_is_admin(message.from_user.id)==True:

        await Advertisment.what_message.set()

        FSM_ikm = ReplyKeyboardRemove()
        await message.answer(text="Яким буде твоє оголошення?\n/cancel - припинити", reply_markup=FSM_ikm)


# ловимо першу відповідь і дивимось на оголошення
async def FSMtext(message: types.Message, state: FSMContext):
    if (message.text == "/cancel"):
        await message.reply("Створення оголошення припинено!", reply_markup=FSM_ikm)
        await state.finish()
    else:
        async with state.proxy() as data:  
            data['message_id'] = message

        await Advertisment.next()
        
        await data['message_id'].send_copy(message.from_id)
        await message.answer('Твоє оголошення буде виглядати так. Відправляємо?')


async def FSMsend(message: types.Message, state: FSMContext):
    if (message.text=="Так"):
        await message.answer("Оголошення буде створено найближчим часом!", reply_markup=FSM_ikm)

        async with state.proxy() as data:
            message = data['message_id']

        all = db.get_all_user_id()

        for user_id in all:
            try:
                await message.send_copy(user_id[0])
                print(f'Відправлено до {user_id[0]}')
            except:
                db.delete_user(user_id[0])

        await state.finish()

    elif (message.text=="Ні"):
        await message.answer("Прийнято! Оголошення не буде відправлено!", reply_markup=FSM_ikm)
        await state.finish()

    else:
        await message.answer("Треба відповісти так або ні!")
        await Advertisment.send_or_not.set()


def my_admin_register_message_handler(dp: Dispatcher):
    dp.register_message_handler(advert, Text(startswith="📢"), state=None)
    dp.register_message_handler(FSMtext, state=Advertisment.what_message)
    dp.register_message_handler(FSMsend, state=Advertisment.send_or_not)

    dp.register_message_handler(admin, commands=['admin'], is_reply=True)
    dp.register_message_handler(noadmin, commands=['noadmin'], is_reply=True)