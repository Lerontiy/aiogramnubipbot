from aiogram import  Dispatcher, types
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from create_bot import bot
from stuff.settings import DEPARTMENTS, WEEKDAYS, SKIP_TR, SUBJECTS
from stuff.database import db
from stuff.marcups import *
from stuff.my_requests import my_request

from bs4 import BeautifulSoup as BS


# блок, коли немає акаунту і треба визначитись з класом (викладач(-ка), студент(-ка))
async def htoya(callback: types.CallbackQuery):
    #try:
    #    await bot.edit_message_text(chat_id=callback.from_user.id,\
    #        message_id=callback.message.message_id, text="Зачекай...")
    #except:
    #    pass
        
    try:
        acc_action = callback.data.split('_')[1]
    except:
        acc_action = "None"


    acc_ikm = InlineKeyboardMarkup()

    acc_ikm.add(InlineKeyboardButton("Я студент(-ка)", callback_data=f"studcourse_{acc_action}"))
    acc_ikm.add(InlineKeyboardButton("Я викладач(-ка)", callback_data=f"teachweekday_{acc_action}"))

    if acc_action=="None":
        text = "«Хто я?»"
    else:
        text = "<b>[Налаштування]</b> «Хто я?»"

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm, parse_mode='html')
    except:
        pass
# /блок, коли немає акаунту і треба визначитись з класом (викладач(-ка), студент(-ка))



# блок для викладачів/викладачок

# день тижня
async def teach_weekday(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')

    acc_action = callback_data[1]

    teach_ikm = InlineKeyboardMarkup()
    teach_ikm = marcup_get_weekdays("teachchoosesubj", acc_action)

    teach_ikm.add(InlineKeyboardButton("« Назад", callback_data=f"htoya_{acc_action}"))

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text="Оберіть потрібний день тижня:", reply_markup=teach_ikm)
    except:
        pass
# /день тижня

# вибір предмета
async def teach_choose_subj(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')

    acc_action = callback_data[1]
    
    teach_ikm = InlineKeyboardMarkup()
    subjects = db.get_user_subjects(callback.from_user.id)

    if (subjects=="") or (acc_action!="None"):
        teach_ikm = marcup_get_all_subjects("teachparse", acc_action=acc_action, subjects=subjects)

        text = "<b>[Налаштування]</b> Оберіть один або декілька предметів"

    else:
        weekday = int(callback_data[2])

        teach_ikm = marcup_get_subjects("teachparse", subjects=subjects, weekday=weekday)

        teach_ikm.add(InlineKeyboardButton("« До вибору дня тижня", callback_data=f"teachweekday_None"))
        text = "Оберіть предмет\n/settings - змінити предмети"

    try:
        return await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=teach_ikm, parse_mode='html')
    except:
        pass
# /вибір предмета

# парсинг розкладу викладачі
async def teach_parse(callback: types.CallbackQuery):
    callback_data = callback.data.split('_')

    weekday = int(callback_data[1])
    subj = callback_data[2]

    teach_ikm = InlineKeyboardMarkup()

    html = my_request.get_weekday_html(weekday)

    groups = [[], [], [], [], []]
    regime = None
    subj = SUBJECTS[subj]
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
                            if (subj in el_td.text) or (("Захист України" in el_td.text) and (subj[-3:-1] in el_td.text)):
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
    
    teach_ikm.add(InlineKeyboardButton("« До вибору предмета", callback_data=f"teachchoosesubj_None_{weekday}"))

    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text="\n".join(send_text), parse_mode="html", reply_markup=teach_ikm)
    except:
        pass

    del send_text, regime, groups, all_groups, subj_count, subj, div, iter_tr, el_tr, iter_td, el_td, html, thtml, dhtml, day_p_mon
    return
# /парсинг розкладу викладачі

# /блок для викладачів/викладачок



# блок для студентів          

# курс
async def stud_course(callback: types.CallbackQuery):
    #await asyncio.sleep(0)
    #try:
    #    await bot.edit_message_text(chat_id=callback.from_user.id,\
    #        message_id=callback.message.message_id, text="Зачекай...")
    #except:
    #    pass

    try:
        callback_data = callback.data.split('_')
        acc_action = callback_data[1]
    except:
        acc_action = 'None'

    acc_ikm = InlineKeyboardMarkup()

    acc_ikm.add(InlineKeyboardButton(text="1 курс", callback_data=f"studdep_1_{acc_action}"), InlineKeyboardButton(text="2 курс", callback_data=f"studdep_2_{acc_action}"))
    acc_ikm.add(InlineKeyboardButton(text="3 курс", callback_data=f"studdep_3_{acc_action}"), InlineKeyboardButton(text="4 курс", callback_data=f"studdep_4_{acc_action}"))

    #acc_ikm.add(InlineKeyboardButton("« Назад", callback_data="htoya"))
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text="Обери свій курс:", reply_markup=acc_ikm)
    except:
        pass
# /курс

# відділення студенти
async def stud_department(callback:types.CallbackQuery):
    #await asyncio.sleep(0)

    #try:
    #    await bot.edit_message_text(chat_id=callback.from_user.id,\
    #        message_id=callback.message.message_id, text="Зачекай...")
    #except:
    #    pass
    
    callback_data = callback.data.split('_')
    course = callback_data[1]
    acc_action = callback_data[2]
    
    all_departments = db.get_all_departments_by_course(course)
    
    acc_ikm = InlineKeyboardMarkup()

    for department in all_departments:
        acc_ikm.add(InlineKeyboardButton(text=DEPARTMENTS[int(department[0])], callback_data=f"studgroup_{course}_{department[0]}_{acc_action}"))
                
    acc_ikm.add(InlineKeyboardButton(text="« До курсів", callback_data=f"studcourse_{acc_action}"))

    #try:
    return await bot.edit_message_text(chat_id=callback.from_user.id,\
        message_id=callback.message.message_id, text="Обери своє відділення:", reply_markup=acc_ikm)
    #except:
    #    pass
# /відділення студенти

# група студенти
async def stud_group(callback: types.CallbackQuery):
    #await asyncio.sleep(0)
    
    #try:
    #    await bot.edit_message_text(chat_id=callback.from_user.id,\
    #        message_id=callback.message.message_id, text="Зачекай...")
    #except:
    #    pass

    callback_data = callback.data.split('_')

    course = callback_data[1]
    department = callback_data[2]
    try:
        acc_action = callback_data[3]
    except:
        acc_action = 'None'
    
    all_groups = db.get_all_groups_by_dep_and_cour(department, course)

    acc_ikm = InlineKeyboardMarkup()

    for group in all_groups:
        if acc_action=='None':
            callback_data = f"studweekday_{group[0]}"
        else:
            callback_data = f"updateacc_0_{group[0]}"
        
        acc_ikm.add(InlineKeyboardButton(text=group[0], callback_data=callback_data))
            
    acc_ikm.add(InlineKeyboardButton(text="« До відділень", callback_data=f"studdep_{course}_{acc_action}"))

    try:
        return await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text="Обери свою групу:", reply_markup=acc_ikm)
    except:
        pass
# /група студенти

# день тижня студенти
async def stud_weekday(callback: types.CallbackQuery | types.Message):
    #try:
    #    await bot.edit_message_text(chat_id=callback.from_user.id,\
    #        message_id=callback.message.message_id, text="Зачекай...")
    #except:
    #    pass


    callback_data = callback.data.split('_')

    group = str(callback_data[1])

    acc_ikm = marcup_get_weekdays("studparse", group)

    department = db.get_department_by_group(group)
    course = db.get_course_by_group(group)

    acc_ikm.add(InlineKeyboardButton("« До груп", callback_data=f"studgroup_{course}_{department}"))
    
    try:
        return await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text="Обери потрібний день тижня:", reply_markup=acc_ikm)
    except:
        pass
# /день тижня студенти

# парсинг розкладу студенти
async def stud_parse(callback:types.CallbackQuery):
    # start_time = time.time()

    callback_data = callback.data.split('_')
    
    group = str(callback_data[1])
    weekday = int(callback_data[2])

    try:
        if callback_data[3]!=None:
            #weekday = 4
            #group = '107-К' 

            studfind_ikm = InlineKeyboardMarkup()
            studfind_ikm.add(InlineKeyboardButton("« До днів тижня", callback_data=f"studweekday_{group}"))

            await bot.edit_message_reply_markup(
                chat_id=callback.from_user.id,\
                message_id=callback.message.message_id,
                reply_markup=studfind_ikm)

            del studfind_ikm
    except:
        pass

    #if db.user_is_admin(callback.from_user.id):
    #    try:
    #        if callback_data[3]!=None:
    #            #weekday = 4
    #            #group = '107-К' 
#
    #            studfind_ikm = InlineKeyboardMarkup()
    #            studfind_ikm.add(InlineKeyboardButton("« До вибору дня тижня", callback_data=f"studweekday_{group}"))
#
    #            await bot.edit_message_reply_markup(
    #                chat_id=callback.from_user.id,\
    #                message_id=callback.message.message_id,
    #                reply_markup=studfind_ikm)
#
    #            del studfind_ikm
    #    except:
    #        pass

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
            if (iter_td==0) and (group in el_td.text):
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
                elif (num == iter_td) and (len(text) < 5):
                    if (el_td.text=="-"):
                        text.append("")
                    else:
                        text.append(el_td.text)
                    k = False
                    if (len(text) == 5):
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
                    if (group[:3]==(el_td.text)[:3]):
                        if (group[:3]=="303") or (group[:3]=="305"):
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
                    InlineKeyboardButton("« До днів тижня", callback_data=f"studweekday_{group}"),\
                    InlineKeyboardButton("Оновити", callback_data=f"studparse_{group}_{weekday}_update"),\
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
async def update_account(callback: types.CallbackQuery):
    #try:
    #    await bot.edit_message_text(chat_id=callback.from_user.id,\
    #        message_id=callback.message.message_id, text="Зачекай...")
    #except:
    #    pass

    callback_data = callback.data.split('_')

    _type = callback_data[1]
    db.update_account(callback_data[2], user_id=callback.from_user.id, _type=_type)

    acc_ikm = InlineKeyboardMarkup()
    if _type=="0":
        text = "Зміни успішно застосовано"
        acc_ikm.add(InlineKeyboardButton("« До налаштувань", callback_data=f"settings"))
    else:
        text = "<b>[Налаштування]</b> Оберіть один або декілька предметів"
        subjects = db.get_user_subjects(callback.from_user.id)
        acc_ikm = marcup_get_all_subjects(acc_action="1", subjects=subjects)
            
    
    try:
        await bot.edit_message_text(chat_id=callback.from_user.id,\
            message_id=callback.message.message_id, text=text, reply_markup=acc_ikm, parse_mode='html')
    except:
        pass


    
    del callback_data, acc_ikm
# /робота з акаунтом


def my_register_callback_query_handler(dp: Dispatcher):
    dp.register_callback_query_handler(htoya, Text(startswith='htoya'))

    #dp.register_callback_query_handler(teachinfo, Text(startswith='teachinfo'))

    dp.register_callback_query_handler(teach_weekday, Text(startswith='teachweekday'))
    dp.register_callback_query_handler(teach_choose_subj, Text(startswith='teachchoosesubj'))
    dp.register_callback_query_handler(teach_parse, Text(startswith='teachparse'))

    dp.register_callback_query_handler(stud_course, Text(startswith='studcourse'))
    dp.register_callback_query_handler(stud_department, Text(startswith='studdep'))
    dp.register_callback_query_handler(stud_group, Text(startswith='studgroup'))
    dp.register_callback_query_handler(stud_weekday, Text(startswith='studweekday'))
    dp.register_callback_query_handler(stud_parse, Text(startswith='studparse'))

    dp.register_callback_query_handler(update_account, Text(startswith='updateacc'))
    