from aiogram import types, Dispatcher
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
#from aiogram.utils.callback_data import CallbackData
from aiogram.dispatcher.filters import Text

from create_bot import bot
from stuff.settings import FSM_ikm
from stuff.marcups import marcup_get_weekdays
from stuff.messages import MESSAGES
import stuff.callback_data as cb_data

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
    await bot.send_message(message.from_user.id, text=MESSAGES["HELP_MESS"])


async def schedule(message: types.Message):
    db.check_user_in_db(message.from_id)

    acc_ikm = InlineKeyboardMarkup(row_width=1)
    
    db.check_user_in_db(message.from_user.id)

    acc_type = db.get_acctype(message.from_user.id)
        
    if (acc_type=="0") or (acc_type=="1"):
        if (acc_type=="0"):
            group = db.get_group(message.from_user.id)

            acc_ikm = marcup_get_weekdays(prefix='studparse', group=group)

            department = db.get_department_by_group(group)
            course = db.get_course_by_group(group)

            clb_data = cb_data.studgroup.new(course=course, department=department, acc_action='None')
            acc_ikm.row(InlineKeyboardButton(MESSAGES['BACK_TO_GROUPS'], callback_data=clb_data))
            
            del group, department, course

        elif (acc_type=="1"):
            acc_ikm = marcup_get_weekdays(prefix="teachchoosesubj", addition='None')

            acc_ikm.row(InlineKeyboardButton(MESSAGES['BACK'], callback_data=cb_data.htoya.new(acc_action='None')))


        await message.answer_photo(photo=open("stuff/timetable.jpg", 'rb'), caption=MESSAGES['CHOOSE_WEEKDAY'], reply_markup=acc_ikm)
            
            
    else:
        acc_ikm.add(InlineKeyboardButton(MESSAGES['IM_STUDENT'], callback_data=cb_data.studcourse.new(acc_action='None')),\
                    InlineKeyboardButton(MESSAGES['IM_TEACHER'], callback_data=cb_data.teachweekday.new(page='0')))

        await message.answer_photo(photo=open("stuff/timetable.jpg", 'rb'), caption=MESSAGES['CHOOSE_WHO_ARE_YOU'], reply_markup=acc_ikm)

        #await message.answer(text=MESSAGES['CHOOSE_WHO_ARE_YOU']+"\n/settings", reply_markup=acc_ikm)

    del acc_ikm, acc_type


# розклад дзвінків
async def timetable(message: types.Message):
    await message.answer_photo(photo=open("stuff/timetable.jpg", 'rb'))
# /розклад дзвінків

# налаштування
async def settings(message: types.Message|types.CallbackQuery):
    #print(type(message))
    db.check_user_in_db(message.from_user.id)

    set_ikm = InlineKeyboardMarkup(row_width=1)

    l = [None, '']

    if db.get_acctype(message.from_user.id) in l:
        text = MESSAGES['CREATE_ACC']
    else:
        text = MESSAGES['UPDATE_ACC']

    set_ikm.row(InlineKeyboardButton(text, callback_data=cb_data.htoya.new(acc_action='update')))
        
    #if (db.user_is_admin(message.from_user.id)):
    #    set_ikm.row(InlineKeyboardButton(text+" (адмін)", callback_data=cb_data.htoya.new(acc_action='update')))

    #await message.answer(MESSAGES['SETTINGS'], reply_markup=set_ikm)
    if type(message)==types.Message:
        await message.answer_photo(photo=open("stuff/settings.png", 'rb'), caption=MESSAGES['SETTINGS'], reply_markup=set_ikm)

        #await bot.send_message(chat_id=message.from_user.id, text=MESSAGES['SETTINGS'], reply_markup=set_ikm)
    else:
        try:
            await bot.edit_message_caption(chat_id=message.from_user.id,\
                message_id=message.message.message_id, caption=MESSAGES['SETTINGS'], reply_markup=set_ikm)
        except:
            try:
                await bot.edit_message_text(chat_id=message.from_user.id,\
                    message_id=message.message.message_id, text=MESSAGES['SETTINGS'], reply_markup=set_ikm)
            except:
                pass

    del set_ikm, l, text
# /налаштування



def my_register_message_handler(dp: Dispatcher):
    dp.register_message_handler(start, commands=['start'], chat_type=['private'])

    dp.register_message_handler(help, commands=['help'], chat_type=['private'])

    dp.register_message_handler(schedule, commands=['schedule'], chat_type=['private'])

    dp.register_message_handler(timetable, commands=['timetable'], chat_type=['private'])

    dp.register_message_handler(settings, commands=['settings'], chat_type=['private'])
    dp.register_callback_query_handler(settings, cb_data.settings.filter())
    