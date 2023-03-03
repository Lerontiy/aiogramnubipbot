from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from stuff.settings import WEEKDAYS, SUBJECTS
from stuff.messages import MESSAGES
import stuff.callback_data as cb_data

import datetime

def marcup_get_all_subjects(prefix:str, acc_action:str, subjects:str, page='0', weekday='None'):
    teach_ikm = InlineKeyboardMarkup(row_width=2)
    subjects = subjects.split('-')
    
    ikm_list = list()
    page_switch_list = list()
    
    page = int(page)
    cut = page*10
    for id in list(SUBJECTS)[cut:cut+10]:
        name = SUBJECTS[id]

        if prefix=='teachparse':
            ikm_list.append((name, cb_data.teachparse.new(subj_id=id, weekday=weekday, update='None', page=str(page))))

        elif prefix=='updateacc':
            if id in subjects:
                _name = '☑️ '+name
            else:
                _name = name
            ikm_list.append((_name, cb_data.updateacc.new(_type='1', addition=id, page=page)))

            del _name


        if page!=0 and len(page_switch_list)==0:
            page_switch_list.append(('«', cb_data.teachchoosesubj.new(acc_action=acc_action, weekday=weekday, page=page-1)))

    try:
        if list(SUBJECTS)[cut+10]:
            page_switch_list.append(('»', cb_data.teachchoosesubj.new(acc_action=acc_action, weekday=weekday, page=page+1)))
    except:
        pass


    if acc_action!="None":
        back_text = MESSAGES["BACK_TO_SETTINGS"]
        back_callback_text = cb_data.settings.new()
    else:
        back_text = MESSAGES["BACK_TO_WEEKDAYS"]
        back_callback_text = cb_data.teachweekday.new(page=page)

    ikm_list = (InlineKeyboardButton(text=name, callback_data=callback_data) for name, callback_data in ikm_list)
    teach_ikm.add(*ikm_list)

    page_switch_list = (InlineKeyboardButton(text=name, callback_data=callback_data) for name, callback_data in page_switch_list)
    teach_ikm.row(*page_switch_list)

    teach_ikm.row(InlineKeyboardButton(text=back_text, callback_data=back_callback_text))

    del subjects, ikm_list, id, name, back_text, back_callback_text

    return teach_ikm


# дні тижня
def marcup_get_weekdays(prefix:str, page:str='0', **addition:str):
    acc_ikm = InlineKeyboardMarkup(row_width=2)
    
    page = int(page)
    ikm_list = list()

    for iter, i in enumerate(WEEKDAYS):
        if (datetime.datetime.today() - datetime.timedelta(hours=0)).weekday()==iter:
            weekday_name = f"{i} - сьогодні"
        else:
            weekday_name = f"{i}"

        if prefix=='studparse':
            callb_data = cb_data.studparse.new(group=addition['group'], weekday=iter, update='None')
        elif prefix=='teachchoosesubj':
            callb_data = cb_data.teachchoosesubj.new(acc_action='None', weekday=iter, page=page)

        ikm_list.append((weekday_name, callb_data))
    
    ikm_list = (InlineKeyboardButton(text=name, callback_data=callback_data) for name, callback_data in ikm_list)
    
    acc_ikm.add(*ikm_list)
    

    del ikm_list, iter, i, weekday_name, callb_data, prefix, addition

    return acc_ikm
# /дні тижня


def marcup_get_subjects(subjects: str, weekday, page):
    teach_ikm = InlineKeyboardMarkup(row_width=2)

    page = int(page)
    cut = page*10

    ikm_list = []
    page_switch_list = []

    page_subj_list = (subjects.split('-'))[cut:cut+10]
    
    if page_subj_list==[]:
        return marcup_get_all_subjects(prefix='teachparse', acc_action='None', subjects=subjects, page=page, weekday=weekday)
    
    for subj_id in page_subj_list:
        ikm_list.append(InlineKeyboardButton(SUBJECTS[subj_id], callback_data=cb_data.teachparse.new(subj_id=subj_id, weekday=weekday, update='None', page=page)))
    
    teach_ikm.add(*ikm_list)

    if page!=0:
        page_switch_list.append(('«', cb_data.teachchoosesubj.new(acc_action='None', weekday=weekday, page=page-1)))

    try:
        if (subjects.split('-'))[cut+10]:
            page_switch_list.append(('»', cb_data.teachchoosesubj.new(acc_action='None', weekday=weekday, page=page+1)))
    except:
        pass

    page_switch_list = (InlineKeyboardButton(text=name, callback_data=callback_data) for name, callback_data in page_switch_list)
    teach_ikm.row(*page_switch_list)

    teach_ikm.row(InlineKeyboardButton(MESSAGES['BACK_TO_WEEKDAYS'], callback_data=cb_data.teachweekday.new(page=page)))

    del ikm_list, subj_id, page_switch_list

    return teach_ikm
