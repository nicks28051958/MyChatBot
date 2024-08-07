import telebot
from telebot import types
import datetime
import time
import threading
bot = telebot.TeleBot('7440534569:AAFXLEs0YZE48EruWrWBXfWJJ9tthP6748Y')
users = {}
@bot.message_handler(commands=['start'])
def start_message(message):
    user_id = message.chat.id
    users.setdefault(user_id, {})
    bot.send_message(user_id, "Привет! Это бот для управления днями рождения. Введите ваше имя:")
@bot.message_handler(func=lambda message: True)
def handle_name(message):
    user_id = message.from_user.id
    if 'name' not in users.get(user_id, {}):
        users.setdefault(user_id, {})
        users[user_id]['name'] = message.text
        bot.send_message(user_id, "Введите дату рождения в формате ДД.ММ.ГГГГ")
    else:
        users[user_id]['name'] = message.text
        handle_birthday(message)
@bot.message_handler(func=lambda message: message.text.isdigit() and len(message.text) == 10)
def handle_birthday(message):
    user_id = message.from_user.id
    if 'name' not in users.get(user_id, {}):
        bot.send_message(user_id, "Пожалуйста, сначала введите ваше имя.")
        return
    birthday = message.text
    day, month, year = map(int, birthday.split('.'))
    if 1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= 2100:
        users[user_id]['birthday'] = birthday
        markup = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton('ЗАГЛЯНЕМ В НЕДАЛЕКОЕ ПРОШЛОЕ?', callback_data='color_purple')
        button2 = types.InlineKeyboardButton('ВАШИ ДРУЗЬЯ И ПОДРУГИ', callback_data='color_blue')
        button3 = types.InlineKeyboardButton('ВАШИ ПОСТУПКИ ПО ОТНОШЕНИЮ К ДРУЗЬЯМ И ПОДРУГАМ', callback_data='color_red')
        markup.add(button1, button2, button3)
        bot.send_message(user_id, "Выберите интересующую вас опцию:", reply_markup=markup)
        threading.Timer(5.0, timeout_message, [user_id]).start()
    else:
        bot.send_message(user_id, "Дата рождения введена некорректно. Попробуйте снова.")
def timeout_message(user_id):
    bot.send_message(user_id, "Время вышло.")

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.message.chat.id
    if call.data == 'color_purple':
        bot.send_message(user_id, "Вы выбрали опцию 'ЗАГЛЯНЕМ В НЕДАЛЕКОЕ ПРОШЛОЕ?'")
    elif call.data == 'color_blue':
        bot.send_message(user_id, "Вы выбрали опцию 'ВАШИ ДРУЗЬЯ И ПОДРУГИ'")
    elif call.data == 'color_red':
        bot.send_message(user_id, "Вы выбрали опцию 'ВАШИ ПОСТУПКИ ПО ОТНОШЕНИЮ К ДРУЗЬЯМ И ПОДРУГАМ'")

    def polling_worker():
        bot.polling()
    def timer_event(user_id, start_time):
        remaining_time = 5 - (time.time() - start_time)
        if remaining_time > 0:
            bot.send_message(user_id, f"Осталось времени: {int(remaining_time)} секунд.")
            threading.Timer(1.0, timer_event, args=(user_id, start_time)).start()
        else:
            bot.send_message(user_id, "Время вышло.")
            threading.Thread(target=polling_worker).start()
            timer_event(user_id, time.time())

print("test")
bot.polling(none_stop=True)
