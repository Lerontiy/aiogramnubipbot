from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import bot
from stuff.settings import WEEKDAYS, FSM_ikm, MESSAGES
from stuff.settings import *
from stuff.marcups import marcup_get_weekdays

from datetime import date

from stuff.database import db

#@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    db.check_user_in_db(message.from_user.id)

    if db.user_is_admin(message.from_user.id)==True:
        reply_markup = FSM_ikm
    else:
        reply_markup = None

    await bot.send_message(message.from_user.id, text=MESSAGES["START_MESS"], reply_markup=reply_markup)


#@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await bot.send_message(message.from_user.id, text=MESSAGES["HELP_MESS"], parse_mode='html')


#@dp.message_handler(commands=['schedule'])
async def schedule(message: types.Message):
    db.check_user_in_db(message.from_user.id)

    group = db.get_group(message.from_user.id)

    
    if (group!=None and group!=""):
        acc_ikm = marcup_get_weekdays("studparse", group)

        department = db.get_department_by_group(group)
        course = db.get_course_by_group(group)

        acc_ikm.add(InlineKeyboardButton("« Назад до груп", callback_data=f"studgroup_{course}_{department}"))

        await bot.send_message(message.from_user.id, text="Обери потрібний день тижня:", reply_markup=acc_ikm, parse_mode="html")

    else:
        acc_ikm = InlineKeyboardMarkup()

        acc_ikm.add(InlineKeyboardButton("1 курс", callback_data=f"studdep_1_None"), InlineKeyboardButton("2 курс", callback_data=f"studdep_2_None"))
        acc_ikm.add(InlineKeyboardButton("3 курс", callback_data=f"studdep_3_None"), InlineKeyboardButton("4 курс", callback_data=f"studdep_4_None"))

        await bot.send_message(message.from_user.id, text="Обери свій курс:", reply_markup=acc_ikm)


async def noschedule(message: types.Message):
    db.check_user_in_db(message.from_id)

    if (db.user_is_admin(message.from_id)):
        #await message.reply(message)
        #await bot.send_photo(photo="AgACAgIAAxkBAAIKhmNe6GvJ_boVFKmcu60eQkx7cjgsAAITxDEbGbX5Si3n-2-h7v1lAQADAgADeAADKgQ", chat_id=message.from_user.id)
        acc_ikm = InlineKeyboardMarkup()
       
        db.check_user_in_db(message.from_user.id)

        acc_type = db.get_acctype(message.from_user.id)
            
            
        if (acc_type=="0"):
            group = db.get_group(message.from_user.id)

            acc_ikm = marcup_get_weekdays("studparse", group)

            await bot.send_message(message.from_user.id, text="Обери потрібний день тижня:", reply_markup=acc_ikm, parse_mode="html")
            

        elif (acc_type=="1"):
            acc_ikm = marcup_get_weekdays("teachchoosesubj", "None")

            acc_ikm.add(InlineKeyboardButton("« Назад", callback_data=f"htoya_None"))

            try:
                await bot.send_message(chat_id=message.from_user.id, text="Обери потрібний день тижня", reply_markup=acc_ikm)
            except:
                pass
                
                
        else:
            acc_ikm.add(InlineKeyboardButton("Я студент", callback_data=f"studcourse"))
            acc_ikm.add(InlineKeyboardButton("Я викладач", callback_data=f"teachchoosesubj_None"))
            
            try:
                await bot.send_message(message.from_user.id, text="Оберіть хто ви:\n(/settings - створити акаунт)", reply_markup=acc_ikm)
            except:
                pass


# розклад дзвінків
async def timetable(message: types.Message):
    await bot.send_photo(photo="AgACAgIAAxkBAAIKhmNe6GvJ_boVFKmcu60eQkx7cjgsAAITxDEbGbX5Si3n-2-h7v1lAQADAgADeAADKgQ", chat_id=message.from_user.id)
# /розклад дзвінків

# налаштування
async def settings(message: types.Message):
    db.check_user_in_db(message.from_id)

    set_ikm = InlineKeyboardMarkup()

    if db.get_acctype(message.from_id)==None:
        text = "Створити новий акаунт"
    else:
        text = "Внести зміни в акаунт"

    set_ikm.add(InlineKeyboardButton(text, callback_data="studcourse_change"))
        
    if (db.user_is_admin(message.from_id)):
        set_ikm.add(InlineKeyboardButton("Внести зміни в акаунт (адмін)", callback_data="htoya_change"))

    await message.answer("Налаштування", reply_markup=set_ikm)
# /налаштування



def my_register_message_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], chat_type=['private'])

    dp.register_message_handler(help, commands=['help'], chat_type=['private'])

    dp.register_message_handler(schedule, commands=['schedule'], chat_type=['private'])
    dp.register_message_handler(noschedule, commands=['noschedule'], chat_type=['private'])

    dp.register_message_handler(timetable, commands=['timetable'], chat_type=['private'])

    dp.register_message_handler(settings, commands=['settings'], chat_type=['private'])
    