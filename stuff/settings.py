from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#нормальний
API_TOKEN = "5403738951:AAEbbME_mAhs9sVAQxvy9KYGG5MjktTfaW8"

#тестовий
#API_TOKEN = "5718594262:AAFrlaZpViF_e2AVCiqQjbh7JqZ9JEzVKR4"

DEPARTMENTS = [
    "Економічне відділення", "Маркетинг і товарознавство", "Комп'ютерна інженерія", 
]

WEEKDAYS = [
    "Понеділок", "Вівторок", "Середа", "Четвер", "П'ятниця", "Субота"
]

SKIP_TR = [
    0, 2, 3, 4, 33, 34
]

ADMINS = [
    706030949,
]

help = ["<b>Базові команди:</b>"]
help.append("/schedule - Подивитися розклад занять")
help.append("/timetable - Подивитися розклад дзвінків")
help.append("/settings - Налаштування")

MESSAGES = {
    "SYS_MESS" : "⚠️ Системне повідомлення!",
    "START_MESS" : """Привіт!\nЯ бот для ВСП «ІФК НУБіП України»\nЯ допоможу тобі довго не шукати розклад занять!\n/help - Путівник""",
    "HELP_MESS" : "\n".join(help)
}
del help

SUBJECTS = {
    "000": "Людина",
    "001": "Захист України д.",
    "002": "Математика",
    "003": "Історія:Україна і світ",
}


FSM_ikm = ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton("📢 Створити оголошення"))

