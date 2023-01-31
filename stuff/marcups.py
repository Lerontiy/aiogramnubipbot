from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from stuff.settings import WEEKDAYS, SUBJECTS

from datetime import date


def marcup_get_all_subjects(*args, acc_action, subjects):
    text = str()
    for el in args:
        text += f"{el}_"

    teach_ikm = InlineKeyboardMarkup()

    buffer = []
    for subj_id in SUBJECTS:
        buffer.append(subj_id)
        if (len(buffer)==2):
            help = help_def(acc_action, buffer, subjects, text)
            addition = help[0]

            
            callback_buffer = help[1]

            teach_ikm.add(InlineKeyboardButton(f"{addition[0]}{SUBJECTS[buffer[0]]}", callback_data=callback_buffer[0]),\
                        InlineKeyboardButton(f"{addition[1]}{SUBJECTS[buffer[1]]}", callback_data=callback_buffer[1]))
            buffer.clear()

    if (len(buffer)==1):
        help = help_def(acc_action, buffer, subjects, text)
        addition = help[0]
        callback_buffer = help[1]

        teach_ikm.add(\
            InlineKeyboardButton("« Назад", callback_data=f"htoya_{acc_action}"),\
            InlineKeyboardButton(f"{addition[0]}{SUBJECTS[buffer[0]]}", callback_data=callback_buffer[0]))
    else:
        teach_ikm.add(InlineKeyboardButton("« Назад", callback_data=f"htoya_{acc_action}"))

    del buffer, text
    return teach_ikm

# допоміжна функція до тої, що зверху
def help_def(acc_action, buffer, subjects, text):
    addition_list = ["", ""]
    callback_buffer = []

    if acc_action=="None":
        for i in range(2):
            callback_buffer.append(f"{text}{buffer[i]}")
    else:
        for iter, sub_id in enumerate(buffer):
            
            if sub_id in subjects.split("-"):
                addition_list[iter] = "☑️ "
            
            callback_buffer.append(f"updateacc_1_{sub_id}")
    
    return (addition_list, callback_buffer)


# дні тижня
def marcup_get_weekdays(*args):
    text = str()
    for el in args:
        text += f"{el}_"

    acc_ikm = InlineKeyboardMarkup()

    buffer = []
    for iter, i in enumerate(WEEKDAYS):
        if date.weekday(date.today()) == iter:
            c = f"{i} - сьогодні"
        else:
            c = f"{i}"
        buffer.append(c)
        if (len(buffer)==2):
            acc_ikm.add(InlineKeyboardButton(buffer[0], callback_data=f"{text}{iter-1}"),\
                        InlineKeyboardButton(buffer[1], callback_data=f"{text}{iter}"))
            buffer.clear()
    del buffer, text

    return acc_ikm
# /дні тижня

def marcup_get_subjects(*args, subjects: str, weekday):
    text = str()
    for el in args:
        text += f"{el}_"
    
    teach_ikm = InlineKeyboardMarkup()

    buffer = []
    for subj_id in subjects.split('-'):
        buffer.append(subj_id)
        if (len(buffer)==2):
            teach_ikm.add(InlineKeyboardButton(SUBJECTS[buffer[0]], callback_data=f"{text}{weekday}_{buffer[0]}"),\
                        InlineKeyboardButton(SUBJECTS[buffer[1]], callback_data=f"{text}{weekday}_{buffer[1]}"))
            buffer.clear()

    if (len(buffer)==1):
        teach_ikm.add(InlineKeyboardButton(SUBJECTS[buffer[0]], callback_data=f"{text}{weekday}_{buffer[0]}"))

    del buffer, text
    return teach_ikm
