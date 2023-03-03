from aiogram.utils.callback_data import CallbackData

htoya = CallbackData('htoya', 'acc_action')

teachweekday = CallbackData('teachweekday', 'page')
teachchoosesubj = CallbackData('teachchoosesubj', 'acc_action', 'weekday', 'page')
teachparse = CallbackData('teachparse', 'subj_id', 'weekday', 'update', 'page')

studcourse = CallbackData('studcourse', 'acc_action')
studdep = CallbackData('studcourse', 'course', 'acc_action')
studgroup = CallbackData('studgroup', 'course', 'department', 'acc_action')
studweekday = CallbackData('studweekday', 'group')
studparse = CallbackData('studparse', 'group', 'weekday', 'update')

updateacc = CallbackData('updateacc', '_type', 'addition', 'page')
settings = CallbackData('settings')