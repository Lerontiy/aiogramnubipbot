from aiogram import  Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import bot
from stuff.settings import DEPARTMENTS, SKIP_TR, SUBJECTS
from stuff.database import db
from stuff.marcups import *
from stuff.my_requests import my_request
from stuff.messages import MESSAGES
import stuff.callback_data as cb_data

import stuff.functions as functions

from bs4 import BeautifulSoup as BS


# блок, коли немає акаунту і треба визначитись з класом (викладач(-ка), студент(-ка))
async def htoya(callback: types.CallbackQuery, callback_data: dict):
    try:
        acc_action = callback_data['acc_action']
    except:
        acc_action = "None"

    acc_ikm = InlineKeyboardMarkup(row_width=1)

    if acc_action=="None":
        clback_data = cb_data.teachweekday.new(page='0')
    else:
        clback_data = cb_data.teachchoosesubj.new(acc_action=acc_action, weekday='None', page='0')

    acc_ikm.add(InlineKeyboardButton(MESSAGES["IM_STUDENT"], callback_data=cb_data.studcourse.new(acc_action=acc_action)),\
                InlineKeyboardButton(MESSAGES["IM_TEACHER"], callback_data=clback_data))


    if acc_action=="None":
        text = MESSAGES["CHOOSE_WHO_ARE_YOU"]+"\n/settings"
    else:
        text = "<b>[Налаштування]</b> "+MESSAGES["CHOOSE_WHO_ARE_YOU"]
        acc_ikm.add(InlineKeyboardButton(MESSAGES["BACK_TO_SETTINGS"], callback_data=cb_data.settings.new()))
        

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm)
    except:
        pass
    
    del acc_action, acc_ikm, clback_data, text

# /блок, коли немає акаунту і треба визначитись з класом (викладач(-ка), студент(-ка))



# блок для викладачів/викладачок

# день тижня
async def teach_weekday(callback: types.CallbackQuery, callback_data:dict):
    page = callback_data['page']

    teach_ikm = marcup_get_weekdays(prefix="teachchoosesubj", page=page)

    teach_ikm.row(InlineKeyboardButton(MESSAGES["BACK"], callback_data=cb_data.htoya.new(acc_action='None')))

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=MESSAGES["CHOOSE_WEEKDAY"], reply_markup=teach_ikm)
    except:
        pass

    del teach_ikm
# /день тижня

# вибір предмета
async def teach_choose_subj(callback: types.CallbackQuery, callback_data:dict):
    acc_action = callback_data['acc_action']
    page = callback_data['page']

    try:
        weekday = callback_data['weekday']
    except:
        weekday="None"

    text = MESSAGES["CHOOSE_SUBJECT(S)"]%(":") # else теж використовує цю змінну
    subjects = db.get_user_subjects(callback.from_user.id)
    
    if acc_action=='None':
        if subjects=='':
            callback_text = "teachparse"
            teach_ikm = marcup_get_all_subjects(prefix=callback_text, acc_action=acc_action, subjects=subjects, weekday=weekday, page=page)
        else:
            teach_ikm = marcup_get_subjects(subjects=subjects, weekday=weekday, page=page)
    else:
        text = "<b>[Налаштування]</b> "+MESSAGES["CHOOSE_SUBJECT(S)"]%("(и). Предмет збережено, якщо біля нього є марка.")
        callback_text = "updateacc"

        teach_ikm = marcup_get_all_subjects(prefix=callback_text, acc_action=acc_action, subjects=subjects, weekday=weekday, page=page)


    #subjects = db.get_user_subjects(callback.from_user.id)
#
    #text = MESSAGES["CHOOSE_SUBJECT(S)"]%(":") # else теж використовує цю змінну
    #if (subjects=="") or (acc_action!="None"):
    #    if acc_action=="None":
    #        callback_text = "teachparse"
    #    else:
    #        text = "<b>[Налаштування]</b> "+MESSAGES["CHOOSE_SUBJECT(S)"]%("(и). Предмет збережено, якщо біля нього є марка.")
    #        callback_text = "updateacc"
    #    
    #    teach_ikm = marcup_get_all_subjects(prefix=callback_text, acc_action=acc_action, subjects=subjects, weekday=weekday, page=page)
    #    
    #else:
    #    teach_ikm = marcup_get_subjects(subjects=subjects, weekday=weekday, page=page)
    #
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=teach_ikm)
    except:
        pass
# /вибір предмета

# парсинг розкладу викладачі
async def teach_parse(callback: types.CallbackQuery, callback_data:dict):
    subj_id = callback_data['subj_id']
    weekday = int(callback_data['weekday'])
    page = callback_data['page']


    try:
        if callback_data['update']!='None':
            teach_ikm = InlineKeyboardMarkup(row_width=2)
            teach_ikm.row(InlineKeyboardButton(MESSAGES["BACK_TO_SUBJECT(S)"], callback_data=cb_data.teachchoosesubj.new(acc_action='None', weekday=weekday, page=page)))

            await bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,\
                message_id=callback.message.message_id,
                reply_markup=teach_ikm)
            del teach_ikm
    except:
        pass


    teach_ikm = InlineKeyboardMarkup(row_width=2)

    html = my_request.get_weekday_html(weekday)

    groups = [[], [], [], [], []]
    regime = None
    subj = SUBJECTS[subj_id]
    day_p_mon = ""

    for div in html.select("#sheets-viewport > div"):
        dhtml = BS(str(div), 'html.parser')
        
        for iter_tr,el_tr in enumerate(dhtml.select("tbody > tr")):
            if (iter_tr in SKIP_TR):
                continue
            else:
                thtml = BS(str(el_tr), 'html.parser')

                for iter_td,el_td in enumerate(thtml.select("td")):
                    if (iter_tr==1) and (iter_td==0) and (day_p_mon==""):
                        data = el_td.text.split(' ')
                        while "" in data: 
                            data.remove("")

                        data = [data[1], data[2]]
                        day_p_mon = " ".join(data)
                        del data
                    elif (iter_td == 0) and (el_td.text==""):
                        all_groups = []
                        regime = "groups"
                        continue
                        
                    elif (regime=="groups"):
                        all_groups.append(el_td.text)
                        continue
                    elif (regime=="check_subj"):
                        try:
                            if functions.in_both_str(subj, el_td.text, string="Захист") and functions.in_both_str(subj, el_td.text, string=subj[-2:-1]) \
                                or functions.in_both_str(subj, el_td.text, string="Історія") \
                                or functions.equal_strings_in_something(subj, el_td.text) \
                                or functions.in_both_str(subj, el_td.text, string="Психологія", excepting_string="етика") \
                                or functions.in_both_str(subj, el_td.text, string="Іноземна мова", excepting_string="спрям") \
                                or functions.in_both_str(subj, el_td.text, string="Українська мова", excepting_string="спрям") \
                                or ((subj in el_td.text) and (subj not in ["Іноземна мова", "Психологія", "Українська мова"])):
                                    groups[subj_count].append(all_groups[iter_td-1])
                        except:
                            pass

                if (regime=="groups"):
                    regime = "check_subj"
                    subj_count = 0
                elif (regime=="check_subj"):
                    subj_count += 1


    send_text = [f"<b>{day_p_mon} {subj}</b>"]

    groups = [", ".join(i) for i in groups]
    
    for iter, el in enumerate(groups):
        send_text.append(f"{iter+1}. {el}")
    
    teach_ikm.row(\
        InlineKeyboardButton(MESSAGES["BACK_TO_SUBJECT(S)"], callback_data=cb_data.teachchoosesubj.new(acc_action='None', weekday=weekday, page=page)),\
        InlineKeyboardButton(MESSAGES["UPDATE"], callback_data=cb_data.teachparse.new(subj_id=subj_id, weekday=weekday, update='update', page=page))
        )

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text="\n".join(send_text), parse_mode="html", reply_markup=teach_ikm)
    except:
        pass

    del subj_id, weekday, teach_ikm, html, groups, regime, subj, day_p_mon, div, dhtml, iter_tr, el_tr, thtml, iter_td, el_td, all_groups

    return
# /парсинг розкладу викладачі

# /блок для викладачів/викладачок



# блок для студентів          

# курс
async def stud_course(callback: types.CallbackQuery, callback_data:dict):
    try:
        acc_action = callback_data['acc_action']
    except:
        acc_action = 'None'

    if acc_action=='None':
        text = MESSAGES["CHOOSE_COURSE"]
    else:
        text = "<b>[Налаштування]</b> "+MESSAGES["CHOOSE_COURSE"]

    acc_ikm = InlineKeyboardMarkup(row_width=2)
    
    
    ikm_list = (InlineKeyboardButton(text=f"{iter} курс", callback_data=cb_data.studdep.new(course=iter, acc_action=acc_action)) for iter in range(1,5))
    acc_ikm.add(*ikm_list)

    acc_ikm.row(InlineKeyboardButton(MESSAGES["BACK"], callback_data=cb_data.htoya.new(acc_action=acc_action)))
    
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm)
    except:
        pass

    del acc_action, text, acc_ikm, ikm_list
# /курс

# відділення студенти
async def stud_department(callback:types.CallbackQuery, callback_data:dict):
    course = callback_data['course']
    acc_action = callback_data['acc_action']

    if acc_action=='None':
        text = MESSAGES["CHOOSE_DEPARTMENT"]
    else:
        text = "<b>[Налаштування]</b> "+MESSAGES["CHOOSE_DEPARTMENT"]
    
    all_departments = db.get_all_departments_by_course(course)
    
    acc_ikm = InlineKeyboardMarkup(row_width=1)

    for department in all_departments: 
        acc_ikm.add(InlineKeyboardButton(text=DEPARTMENTS[int(department[0])], callback_data=cb_data.studgroup.new(course=course, department=department[0], acc_action=acc_action)))
                
    acc_ikm.row(InlineKeyboardButton(text=MESSAGES["BACK_TO_COURSES"], callback_data=cb_data.studcourse.new(acc_action)))

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm)
    except:
        pass
# /відділення студенти

# група студенти
async def stud_group(callback: types.CallbackQuery, callback_data:dict):
    course = callback_data['course']
    department = callback_data['department']
    try:
        acc_action = callback_data['acc_action']
    except:
        acc_action = 'None'

    if acc_action=='None':
        text = MESSAGES['CHOOSE_GROUP']
    else:
        text = "<b>[Налаштування]</b> "+MESSAGES['CHOOSE_GROUP']
    
    all_groups = db.get_all_groups_by_dep_and_cour(department, course)

    acc_ikm = InlineKeyboardMarkup(row_width=1)

    for group in all_groups:
        if acc_action=='None':
            clback_data = cb_data.studweekday.new(group=group[0])
        else:
            clback_data = cb_data.updateacc.new(_type='0', addition=group[0], page='0')
        
        acc_ikm.add(InlineKeyboardButton(text=group[0], callback_data=clback_data))
            
    acc_ikm.row(InlineKeyboardButton(text=MESSAGES["BACK_TO_DEPARTMENTS"], callback_data=cb_data.studdep.new(course=course, acc_action=acc_action)))

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm)
    except:
        pass
# /група студенти

# день тижня студенти
async def stud_weekday(callback: types.CallbackQuery | types.Message, callback_data:dict):
    group = str(callback_data['group'])

    acc_ikm = marcup_get_weekdays(prefix="studparse", group=group)

    department = db.get_department_by_group(group)
    course = db.get_course_by_group(group)

    acc_ikm.row(InlineKeyboardButton(MESSAGES["BACK_TO_GROUPS"], callback_data=cb_data.studgroup.new(course=course, department=department, acc_action='None')))
    
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=MESSAGES["CHOOSE_WEEKDAY"], reply_markup=acc_ikm)
    except:
        pass

    del group, acc_ikm, department, course
# /день тижня студенти

# парсинг розкладу студенти
async def stud_parse(callback:types.CallbackQuery, callback_data:dict):    
    # start_time = time.time()
    group = str(callback_data['group'])
    weekday = int(callback_data['weekday'])

    try:
        if callback_data['update']!="None":
            #weekday = 4
            #group = '107-К' 

            studfind_ikm = InlineKeyboardMarkup()
            studfind_ikm.add(InlineKeyboardButton(MESSAGES["BACK_TO_WEEKDAYS"], callback_data=cb_data.studweekday.new(group=group)))

            await bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,\
                message_id=callback.message.message_id,
                reply_markup=studfind_ikm)

            del studfind_ikm
    except:
        pass

    dep = db.get_department_by_group(group)

    html = my_request.get_weekday_html(weekday)

    # ЕВ/Маркетинг/КІ/Аудиторії
    for iter,el in enumerate(html.select("#sheet-menu > li")):
        if iter == int(dep):
            num = iter
            break
    del iter, el

    for iter,el in enumerate(html.select("#sheets-viewport > div")):
        if (iter==num):
            div = el
        elif (iter==3):
            aud_div = el
    del iter, el, num


    # робота з потрібним блоком розкладу дзвінків
    aud_text = []
    html = BS(str(aud_div), 'html.parser')
    can_write = False
    can_stop = False

    for iter_tr,el_tr in enumerate(html.select("tbody > tr")):
        thtml = BS(str(el_tr), 'html.parser')
        for iter_td,el_td in enumerate(thtml.select("td")):
            if (iter_td==0) and (group[:3] in el_td.text) and (iter_tr>2):
                if (group[:3]=="303") or (group[:3]=="305"):
                    if (group[-1]==el_td.text[-1]):
                        can_write = True
                        continue
                else:
                    can_write = True
                    continue
            elif (can_write):
                if (el_td.text==""):
                    aud_text.append("")
                else:
                    aud_text.append(f"{el_td.text}")
                if (len(aud_text)==5):
                    can_stop = True
                    break
        if (can_stop):
            break
                
    # робота з потрібним блоком занять
    num = -1
    text = []
    html = BS(str(div), 'html.parser')
    can_stop = False
    k = False

    for iter_tr,el_tr in enumerate(html.select("tbody > tr")):
        if (iter_tr in SKIP_TR):
            continue
        else:
            thtml = BS(str(el_tr), 'html.parser')
            for iter_td,el_td in enumerate(thtml.select("td")):
                if (iter_td == 0) and (num < 0):
                    try: 
                        s = int(el_td.text)
                        del s
                        break
                    except:
                        if (iter_tr==1) and (iter_td==0):
                            data = el_td.text.split(' ')
                            while "" in data: 
                                data.remove("")

                            data = [data[1], data[2]]
                            day_p_mon = " ".join(data)
                            del data
                elif (num==iter_td) and (len(text) < 5):
                    if (el_td.text=="-"):
                        text.append("")
                    else:
                        text.append(el_td.text)
                    k = False
                    if (len(text)==5):
                        can_stop = True
                        break
                    else:
                        continue
                elif (num-1 == iter_td) and (num > 0) and (len(text) < 5):
                    if (k==True):
                        if (el_td.text=="-"):
                            text.append("")
                        else:
                            text.append(m)
                    m = el_td.text
                    k = True
                try:
                    if (group[:3] in el_td.text) and (iter_tr>2):
                        if (group[:3] in ["303", "305"]):
                            if (group[-1]==el_td.text[-1]):
                                num = iter_td
                                break
                        else:
                            num = iter_td
                            break
                except:
                    pass
            if (can_stop):
                break
                    
    # b = [f"<b>{day_p_mon} {group}</b>"]
    # for el in text:
    #     b.append(f"{el}")
    # b = "\n".join(b)

    send_text = [f"<b>{day_p_mon} {group}</b>"]
    for iter_les, el_les in enumerate(text):
        if (len(aud_text)==0):
            if (el_les==""):
                send_text.append(f"{iter_les+1}.")
            else:
                send_text.append(f"{iter_les+1}. {el_les}")
        else:
            if (aud_text[iter_les]=="") or (aud_text[iter_les]=="-") or (el_les=="") or (el_les=="-"):
                if (el_les==""):
                    send_text.append(f"{iter_les+1}.")
                else:
                    send_text.append(f"{iter_les+1}. {el_les}")
            else:
                if(("/" in aud_text[iter_les]) or ("." in aud_text[iter_les])):
                    send_text.append(f"{iter_les+1}. {el_les} - {aud_text[iter_les]}")
                else:
                    send_text.append(f"{iter_les+1}. {el_les} - {aud_text[iter_les]} ауд.")

    send_text = "\n".join(send_text)

    studfind_ikm = InlineKeyboardMarkup()
    studfind_ikm.add(\
                    InlineKeyboardButton(MESSAGES["BACK_TO_WEEKDAYS"], callback_data=cb_data.studweekday.new(group=group)),\
                    InlineKeyboardButton(MESSAGES["UPDATE"], callback_data=cb_data.studparse.new(group=group, update='update', weekday=weekday)),\
                    )
    
    
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=send_text, reply_markup=studfind_ikm, parse_mode="html")
    except:
        pass


    del num, thtml, el_tr, el_td, iter_td, html, text, studfind_ikm, weekday, group
            
# /парсинг розкладу студенти
# /блок для студентів



# робота з акаунтом
async def update_account(callback: types.CallbackQuery, callback_data:dict):
    _type = callback_data['_type']
    page = callback_data['page']

    db.update_account(addition=callback_data['addition'], user_id=callback.from_user.id, _type=_type)

    acc_ikm = InlineKeyboardMarkup()
    if _type=="0":
        text = MESSAGES["CHANGES_APPLIED"]
        acc_ikm.add(InlineKeyboardButton(MESSAGES["BACK_TO_SETTINGS"], callback_data=cb_data.settings.new()))
    else:
        text = "<b>[Налаштування]</b> "+MESSAGES["CHOOSE_SUBJECT(S)"]%("(и). Предмет збережено, якщо біля нього є марка.")
        subjects = db.get_user_subjects(callback.from_user.id)
        acc_ikm = marcup_get_all_subjects(prefix='updateacc', acc_action="1", subjects=subjects, page=page)
            
    
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm)
    except:
        pass


    
    del callback_data, acc_ikm
# /робота з акаунтом


def my_register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(htoya, cb_data.htoya.filter())

    #dp.register_callback_query_handler(teachinfo, cb_data.teachinfo.filter())

    dp.register_callback_query_handler(teach_weekday, cb_data.teachweekday.filter())
    dp.register_callback_query_handler(teach_choose_subj, cb_data.teachchoosesubj.filter())
    dp.register_callback_query_handler(teach_parse, cb_data.teachparse.filter())

    dp.register_callback_query_handler(stud_course, cb_data.studcourse.filter())
    dp.register_callback_query_handler(stud_department, cb_data.studdep.filter())
    dp.register_callback_query_handler(stud_group, cb_data.studgroup.filter())
    dp.register_callback_query_handler(stud_weekday, cb_data.studweekday.filter())
    dp.register_callback_query_handler(stud_parse, cb_data.studparse.filter())

    dp.register_callback_query_handler(update_account, cb_data.updateacc.filter())
    