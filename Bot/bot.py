import telebot
from utils import (finder, replace_text, replace_first_word, replace_last_word,
                   replace_first_word_amount, replace_last_word_amount)
from telebot import types
import requests
import sqlite3
from text_to_speech import text_to_speech, speech_to_text
from text_recognition import text_recognition
from wiki import search_wiki, page_wiki


token = '7531354776:AAHStSiRCE65LYDgNv65kOFRjDphEsEWWKs'
bot = telebot.TeleBot(token)

text = '' # Переменная для хранения текста в котором нужно будет выполнить поиск
word = '' # Переменная для хранения слова которое нужно будет искать
text_file = '' # переменная для определения типа текста текст/файл/картинка

name = '' # Переменная для хранения логина текущего пользователя

lang = ''# Переменная с названием языка для создания голоса из текста

replace_word = ''# Слово на которое нужно поменять в замене
find_word = ''# Слово которое нужно заменить
all_or_one = '' # Все вхождения или только 1
another_amount = '' # другое количество слов которые нужно заменить
start_or_finish = '' # искать с конца или сначала

red = False # Заменить слова в тексте или нет

# Переменные для редактирования поиска
regist = False # Регистр
accurate_search = False # Неточный поиск
many_files = False # Поиск во всех текстах
edit_text = False # Считать количество ошибок

message_id = {} # Айди сообщения

all_texts = [] # Список со всеми ранее введенными текстамм

reg_log_user = True # Пользователь регистрируется или авторизируется

isauthenticated = False # Пользователь авторизован

default_balance = 5 # Начальный баланс новых пользователей

topup_balance = 0 # сумма поплнения баланса

author_name = 'Евгений' # Имя автора и банковского получателя

now_balance = 0 # Текущий баланс

"""
Начальная команда
"""
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Добавить пользователя👤")
    item2 = types.KeyboardButton("Начать работу")
    markup.add(item2)
    markup.add(item1)
    bot.send_message(message.chat.id, 'Выберите действие', reply_markup=markup)
    bot.register_next_step_handler(message, user_start)

"""
Начать работу или добавить пользователя
"""
def user_start(message):
    if message.text == 'Начать работу':
        main(message)
    elif message.text == 'Добавить пользователя👤':
        reg_log(message)

"""
Список главных функции бота
"""
@bot.message_handler(commands=['work'])
def main(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Написать текст в ручную✍️")
    item2 = types.KeyboardButton("Отправить файл📄")
    item3 = types.KeyboardButton("Отправить гс🔊")
    item5 = types.KeyboardButton("Отправить картинку🖼️")
    item6 = types.KeyboardButton("Настроить поиск🔎")
    item7 = types.KeyboardButton("Дополнительные возможности")
    item8 = types.KeyboardButton("Назад↪️")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    markup.add(item5)
    markup.add(item6)
    markup.add(item7)
    markup.add(item8)
    bot.send_message(message.chat.id, 'Выберите вариант отправки текст', reply_markup=markup)
    bot.register_next_step_handler(message, variant)


"""
Настройки поиска
Проверяет статус настроек и выводит сообщение с настройками
"""
@bot.message_handler(commands=['search'])
def search(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Учитывать регистр")
    item2 = types.KeyboardButton("Неточный поиск")
    item3 = types.KeyboardButton("Поиск во всех ранее введенных текстах")
    item4 = types.KeyboardButton("Находить слова с ошибкой")
    item5 = types.KeyboardButton("Назад↪️")
    markup.add(item1, item3)
    markup.add(item2, item4)
    markup.add(item5)
    bot.send_message(message.chat.id, 'Выберите настройки')
    if regist == True:
        message1 = 'Учитывать регистр: ✅'
    else:
        message1 = 'Учитывать регистр: ❌'
    if accurate_search == True:
        message2 = 'Неточный поиск: ✅'
    else:
        message2 = 'Неточный поиск: ❌'
    if many_files == True:
        message3 = 'Поиск по всем файлам: ✅'
    else:
        message3 = 'Поиск по всем файлам: ❌'
    if edit_text == True:
        message4 = 'Находить слова с ошибкой: ✅'
    else:
        message4 = 'Находить слова с ошибкой: ❌'

    bot.send_message(message.chat.id, f'Текущие настройки поиска: \n\n {message1} \n\n {message2}\n\n'
                                      f' {message3} \n\n {message4}', reply_markup=markup)

    bot.register_next_step_handler(message, edit_search)

def edit_search(message):
    global regist
    global accurate_search
    global many_files
    global edit_text

    if message.text == 'Учитывать регистр':
        if regist == True:
            regist = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)

        else:
            regist = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
    elif message.text == 'Неточный поиск':
        if accurate_search == True:
            accurate_search = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
        else:
            accurate_search = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
    elif message.text == 'Поиск во всех ранее введенных текстах':
        if many_files == True:
            many_files = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
        else:
            many_files = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
    elif message.text == 'Находить слова с ошибкой':
        if edit_text == True:
            edit_text = False
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
        else:
            edit_text = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            item3 = types.KeyboardButton("Настроить поиск🔎")
            markup.add(item1)
            markup.add(item2)
            markup.add(item3)
            bot.send_message(message.chat.id, 'Изменения сохранены', reply_markup=markup)
            bot.register_next_step_handler(message, variant)
    elif message.text == 'Назад↪️':
        main(message)


def reg_log(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Регистрация")
    item2 = types.KeyboardButton("Авторизация")
    markup.add(item1)
    markup.add(item2)
    bot.send_message(message.chat.id, "Выберите действие", reply_markup=markup)
    bot.register_next_step_handler(message, adduser)

@bot.message_handler(commands=['adduser'])
def adduser(message):
    global reg_log_user
    if message.text == 'Регистрация':
        reg_log_user = True
    elif message.text == 'Авторизация':
        reg_log_user = False
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Назад↪️")
    markup.add(item1)

    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        login TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL,
        balance FLOAT NOT NULL
    )""")

    conn.commit()
    cur.close()
    conn.close()

    bot.send_message(message.chat.id, "Введите имя", reply_markup=markup)
    bot.register_next_step_handler(message, username)


def username(message):
    global name
    if message.text != 'Назад↪️':
        name = message.text.strip()
        bot.send_message(message.chat.id, "Введите пароль")
        bot.register_next_step_handler(message, userpass)
    else:
        start(message)

def check_name(name):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = ?", (name, ))
    user = cur.fetchone()
    conn.close()
    return user

def check_name_login(name, password):
    conn = sqlite3.connect('database.sql')
    cur = conn.cursor()
    cur.execute("SELECT * FROM users WHERE login = ? AND password = ?", (name, password))
    user = cur.fetchone()
    conn.close()
    return user

def userpass(message):
    global isauthenticated
    password = message.text.strip()

    if reg_log_user == True:
        if check_name(name):

            bot.send_message(message.chat.id, "Пользователь с таким именем существует")
        else:

            conn = sqlite3.connect('database.sql')
            cur = conn.cursor()

            cur.execute('INSERT INTO users (login, password, balance) VALUES (?, ?, ?)', (name, password, default_balance))
            conn.commit()
            cur.close()
            conn.close()

            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Список пользователей')
            item2 = types.KeyboardButton('Назад')
            markup.add(item1)
            markup.add(item2)
            bot.send_message(message.chat.id, 'Вы зарегистрированы', reply_markup=markup)
            isauthenticated = True
            bot.register_next_step_handler(message, callback)
    elif reg_log_user == False:
        if check_name_login(name, password):
            bot.send_message(message.chat.id, "Вы успешно авторизовались")
            isauthenticated = True
            bot.register_next_step_handler(message, callback)

        else:
            bot.send_message(message.chat.id, "Неправильные данные")
            bot.register_next_step_handler(message, callback)


def callback(message):
    if message.text == 'Список пользователей':
        conn = sqlite3.connect('database.sql')
        cur = conn.cursor()

        cur.execute('SELECT * FROM users')
        users = cur.fetchall()

        info = 'Пользователи:\n'
        amount = 0
        for i in users:
            info += f'Имя: {i[1]}\n'
            amount += 1
        info += f'Всего пользователей: {amount}'

        cur.close()
        conn.close()

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Добавить пользователя👤")
        item2 = types.KeyboardButton("Начать работу")
        markup.add(item2)
        markup.add(item1)

        bot.send_message(message.chat.id,  info, reply_markup=markup)

        bot.register_next_step_handler(message, user_start)
    else:
        start(message)

@bot.message_handler(commands=['Редактировать'])
def variant(message):
    global text_file
    global text
    if message.text == 'Написать текст в ручную✍️':
        text = ''
        text_file = 'Написать текст в ручную✍️'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад↪️")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Отправьте текст в котором необходимо выполнить поиск',
                         reply_markup=markup)
        bot.register_next_step_handler(message, reverse)

    elif message.text == 'Отправить файл📄':
        text = ''
        text_file = 'Отправить файл📄'
        bot.send_message(message.chat.id, 'Отправьте файл в котором необходимо выполнить поиск',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Отправить гс🔊':
        text = ''
        text_file = 'Отправить гс🔊'
        bot.send_message(message.chat.id, 'Отправьте гс в котором необходимо выполнить поиск',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Отправить картинку🖼️':
        text = ''
        text_file = 'Отправить картинку🖼️'
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад↪️")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Отправьте картинку в которой необходимо выполнить поиск',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_photo)
    elif message.text == "Настроить поиск🔎":
        search(message)
    elif message.text == "Дополнительные возможности":
        possibilites(message)
    elif message.text == "Назад↪️":
        start(message)
    elif text_file == 'Написать текст в ручную✍️':
        text = ''
        bot.send_message(message.chat.id, 'Отправьте новый текст в котором необходимо выполнить поиск',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif text_file == 'Отправить файл📄':
        text = ''
        bot.send_message(message.chat.id, 'Отправьте новый файл в котором необходимо выполнить поиск',
                         reply_markup=telebot.types.ReplyKeyboardRemove())

def reverse(message):
    if message.text == 'Назад↪️':
        main(message)
    else:
        func_text(message)

@bot.message_handler(content_types='text')
def func_text(message):
    global word
    global text
    global text_file
    if red == False:
        if text_file == 'Написать текст в ручную✍️':
            if text == '':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Редактировать')
                markup.add(item1)
                text = message.text
                all_texts.append(text + '\n')
                msg = bot.send_message(message.chat.id, 'Отправьте слово которое нужно найти', reply_markup=markup)
                message_id[message.chat.id] = msg.message_id
                bot.register_next_step_handler(message, edit)

            else:
                word = message.text
            if word != '':
                res = finder(text, word, regist, accurate_search, edit_text, all_texts, many_files)
                if res != []:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Начать заново')
                    markup.add(item1)
                    amount = len(res)
                    finish_res = [str(res[i - 1])   for i in range(1, len(res) + 1)]
                    bot.send_message(message.chat.id, f'Вот что удалось найти: \n {'\n'.join(finish_res)}'
                                                      f' \n Найдено предложений: {amount}', reply_markup=markup)
                    text = ''
                    word = ''
                    bot.register_next_step_handler(message, edit)
                else:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Начать заново')
                    markup.add(item1)
                    bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
                    text = ''
                    word = ''
                    bot.register_next_step_handler(message, edit)

        if text_file == 'Отправить файл📄':
            word = message.text
            res = finder(text, word, regist, accurate_search, edit_text, all_texts, many_files)
            if res != []:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Начать заново')
                markup.add(item1)
                amount = len(res)
                finish_res = [str(res[i - 1]) for i in range(1, len(res) + 1)]
                bot.send_message(message.chat.id, f'Вот что удалось найти: \n {'\n'.join(finish_res)}'
                                                  f' \n Найдено предложений: {amount}', reply_markup=markup)
                text = ''
                word = ''
                bot.register_next_step_handler(message, edit)


            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Начать заново')
                markup.add(item1)
                bot.send_message(message.chat.id, 'В файле нет такого слова', reply_markup=markup)
                text = ''
                word = ''
                bot.register_next_step_handler(message, edit)

        if text_file == 'Отправить картинку🖼️':
            word = message.text
            res = finder(text, word, regist, accurate_search, edit_text, all_texts, many_files)
            if res != []:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Начать заново')
                markup.add(item1)
                amount = len(res)
                finish_res = [str(res[i - 1]) for i in range(1, len(res) + 1)]
                bot.send_message(message.chat.id, f'Вот что удалось найти: \n {'\n'.join(finish_res)} \n'
                                                  f' Найдено предложений: {amount}', reply_markup=markup)
                text = ''
                word = ''
                bot.register_next_step_handler(message, edit)


            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Начать заново')
                markup.add(item1)
                bot.send_message(message.chat.id, 'В картинке нет такого слова', reply_markup=markup)
                text = ''
                word = ''
                bot.register_next_step_handler(message, edit)

def edit(message):
    if message.text == "Редактировать":
        variant(message)
    elif message.text == "Начать заново":
        start(message)
    else:
        func_text(message)

@bot.message_handler(commands=['speech'])
def possibilites(message):
    global isauthenticated
    global now_balance
    if isauthenticated == True:
        now_balance = user_balance(name)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Преобразовать текст в гс🔊')
        item2 = types.KeyboardButton('Заменить слова в тексте')
        item4 = types.KeyboardButton('Википедия')
        item5 = types.KeyboardButton('Пополнить баланс')
        item6 = types.KeyboardButton('Назад↪️')
        markup.add(item1)
        markup.add(item2)
        markup.add(item4)
        markup.add(item5)
        markup.add(item6)
        bot.send_message(message.chat.id, f'Ваш баланс: {now_balance}р\n\nКаждая функция стоит 1р')
        bot.send_message(message.chat.id, 'Выберите', reply_markup=markup)
        bot.register_next_step_handler(message, lang_var)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Авторизоваться')
        markup.add(item1)
        bot.send_message(message.chat.id, "Сначала необходимо авторизоваться", reply_markup=markup)
        bot.register_next_step_handler(message, reg_log)

def lang_var(message):
    global now_balance
    global red
    now_balance = user_balance(name)
    if message.text == 'Преобразовать текст в гс🔊':
        if now_balance >= 1:
            conn = sqlite3.connect('database.sql')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = ? WHERE login = ?", (now_balance - 1, name))
            conn.commit()
            conn.close()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('en')
            item2 = types.KeyboardButton('ru')
            markup.add(item1, item2)
            bot.send_message(message.chat.id, f'Ваш баланс: {now_balance - 1}р')
            bot.send_message(message.chat.id, 'Выберите язык', reply_markup=markup)
            bot.register_next_step_handler(message, poss_var)
        else:
            bot.send_message(message.chat.id, f'Пополните баланс\n Ваш баланс: {now_balance}р')
            bot.register_next_step_handler(message, main)


    elif message.text == 'Заменить слова в тексте':
        if now_balance >= 1:
            conn = sqlite3.connect('database.sql')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = ? WHERE login = ?", (now_balance - 1, name))
            conn.commit()
            conn.close()
            red = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Написать текст в ручную✍️")
            item2 = types.KeyboardButton("Отправить файл📄")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, f'Ваш баланс: {now_balance - 1}р')
            bot.send_message(message.chat.id, 'Выберите', reply_markup=markup)
            bot.register_next_step_handler(message, red_var)
        else:
            bot.send_message(message.chat.id, f'Пополните баланс\n Ваш баланс: {now_balance}р')
            bot.register_next_step_handler(message, main)

    elif message.text == 'Википедия':
        if now_balance >= 1:
            conn = sqlite3.connect('database.sql')
            cursor = conn.cursor()
            cursor.execute("UPDATE users SET balance = ? WHERE login = ?", (now_balance - 1, name))
            conn.commit()
            conn.close()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Назад↪️')
            markup.add(item1)
            bot.send_message(message.chat.id, f'Ваш баланс: {now_balance - 1}р')
            bot.send_message(message.chat.id, 'Напишите то что хотите найти',
                             reply_markup=markup)
            bot.register_next_step_handler(message, wiki)
        else:
            bot.send_message(message.chat.id, f'Пополните баланс\n Ваш баланс: {now_balance}р')
            bot.register_next_step_handler(message, main)

    elif message.text == 'Пополнить баланс':

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        now_balance = user_balance(name)
        item1 = types.KeyboardButton("5р")
        item2 = types.KeyboardButton("10р")
        item3 = types.KeyboardButton("20р")
        item4 = types.KeyboardButton("50р")
        item5 = types.KeyboardButton("Назад")
        markup.add(item1)
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        markup.add(item5)
        bot.send_message(message.chat.id, f"Текущий баланс {now_balance}р", reply_markup=markup)
        bot.send_message(message.chat.id, "Выберите сумму платежа", reply_markup=markup)
        bot.register_next_step_handler(message, check_pay)
    elif message.text == 'Назад↪️':
        main(message)

def user_balance(name):
    conn = sqlite3.connect('database.sql')
    cursor = conn.cursor()
    cursor.execute("SELECT balance FROM users WHERE login = ?", (name,))
    result = cursor.fetchone()
    conn.close()
    print(result[0])
    return result[0]

def check_pay(message):
    global topup_balance
    if message.text == '5р':
        topup_balance = 5
        bot.send_message(message.chat.id, f'Переведите {topup_balance} на '
                                          f'\n 2200 7009 8568 2680\n Хохлов Евгений Васильевич\n и отправьте скрин'
                                          f' на котором видно имя получателя и номер карты',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == '10р':
        topup_balance = 10
        bot.send_message(message.chat.id, f'Переведите {topup_balance} на '
                                          f'\n 2200 7009 8568 2680\n Хохлов Евгений Васильевич\n и отправьте скрин'
                                          f' на котором видно имя получателя и номер карты',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == '20р':
        topup_balance = 20
        bot.send_message(message.chat.id, f'Переведите {topup_balance} на '
                                          f'\n 2200 7009 8568 2680\n Хохлов Евгений Васильевич\n и отправьте скрин'
                                          f' на котором видно имя получателя и номер карты',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == '50р':
        topup_balance = 50
        bot.send_message(message.chat.id, f'Переведите {topup_balance} на '
                                          f'\n 2200 7009 8568 2680\n Хохлов Евгений Васильевич\n и отправьте скрин'
                                          f' на котором видно имя получателя и номер карты',
                         reply_markup=telebot.types.ReplyKeyboardRemove())
    elif message.text == 'Назад':
        possibilites(message)

@bot.callback_query_handler(func=lambda call: call.data)
def answer(call):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton('Начать заново')
    markup.add(item1)
    title, summary, url = page_wiki(call.data)
    bot.send_message(call.message.chat.id, title)
    bot.send_message(call.message.chat.id, summary)
    bot.send_message(call.message.chat.id, url, reply_markup=markup)
    bot.register_next_step_handler(call.message, edit)

def red_var(message):
    global text_file
    if message.text == 'Написать текст в ручную✍️':
        text_file = 'Написать текст в ручную✍️'
        bot.send_message(message.chat.id, 'Введите текст в котором нужно заменить слово')
        bot.register_next_step_handler(message, edit_var)
    if message.text == 'Отправить файл📄':
        text_file = 'Отправить файл📄'
        bot.send_message(message.chat.id, 'Отправьте файл в котором нужно заменить слово')

def edit_var(message):
    global text, text_file, find_word, replace_word, red, all_or_one, another_amount, start_or_finish
    if red == True:
        if text_file == 'Написать текст в ручную✍️':
            if text == '':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Редактировать')
                markup.add(item1)
                text = message.text
                all_texts.append(text + '\n')
                msg = bot.send_message(message.chat.id, 'Отправьте слово которое нужно найти', reply_markup=markup)
                message_id[message.chat.id] = msg.message_id
                bot.register_next_step_handler(message, edit_var)

            elif find_word == '':
                find_word = message.text
                bot.send_message(message.chat.id, 'Отправьте слово на которое нужно поменять')
                bot.register_next_step_handler(message, edit_var)

            elif replace_word == "":
                replace_word = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Все вхождения')
                item2 = types.KeyboardButton('Первое')
                item3 = types.KeyboardButton('Последнее')
                item4 = types.KeyboardButton('Другой вариант')
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)
                bot.send_message(message.chat.id, 'Выберите что нужно заменять', reply_markup=markup)
                bot.register_next_step_handler(message, edit_var)
            elif all_or_one == "":
                all_or_one = message.text
                if all_or_one == 'Все вхождения':
                    res = replace_text(text, find_word, replace_word)
                    if res != []:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Начать заново')
                        markup.add(item1)
                        bot.send_message(message.chat.id, res, reply_markup=markup)
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, edit)
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Начать заново')
                        markup.add(item1)
                        bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, edit)
                elif all_or_one == 'Первое':
                    res = replace_first_word(text, find_word, replace_word)
                    if res != []:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Начать заново')
                        markup.add(item1)
                        bot.send_message(message.chat.id, res, reply_markup=markup)
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, edit)
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Начать заново')
                        markup.add(item1)
                        bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, edit)
                elif all_or_one == 'Последнее':
                    res = replace_last_word(text, find_word, replace_word)
                    if res != []:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Начать заново')
                        markup.add(item1)
                        bot.send_message(message.chat.id, res, reply_markup=markup)
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, edit)
                    else:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Начать заново')
                        markup.add(item1)
                        bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, edit)
                elif all_or_one == 'Другой вариант':
                    bot.send_message(message.chat.id, 'Отправьте число - количество замен')
                    bot.register_next_step_handler(message, edit_var)
            elif another_amount == '' :
                if message.text.isdigit():
                    another_amount = int(message.text)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('С начала')
                    item2 = types.KeyboardButton('С конца')
                    markup.add(item1)
                    markup.add(item2)
                    bot.send_message(message.chat.id, 'Откуда начинать замены', reply_markup=markup)
                    bot.register_next_step_handler(message, edit_var)
                elif message.text.isdigit() == False:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Начать заново')
                    markup.add(item1)
                    bot.send_message(message.chat.id, 'Вы ввели не число', reply_markup=markup)
                    text = ''
                    find_word = ''
                    replace_word = ''
                    all_or_one = ''
                    bot.register_next_step_handler(message, edit)
            elif start_or_finish == '':
                    start_or_finish = message.text
                    if start_or_finish == 'С начала':
                        res = replace_first_word_amount(text, find_word, replace_word, another_amount)
                        if res != []:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Начать заново')
                            markup.add(item1)
                            bot.send_message(message.chat.id, res, reply_markup=markup)
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                            bot.register_next_step_handler(message, edit)
                        else:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Начать заново')
                            markup.add(item1)
                            bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                            bot.register_next_step_handler(message, edit)
                    elif start_or_finish == 'С конца':
                        res = replace_last_word_amount(text, find_word, replace_word, another_amount)
                        if res != []:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Начать заново')
                            markup.add(item1)
                            bot.send_message(message.chat.id, res, reply_markup=markup)
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                            bot.register_next_step_handler(message, edit)
                        else:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Начать заново')
                            markup.add(item1)
                            bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                            bot.register_next_step_handler(message, edit)

        if text_file == 'Отправить файл📄':
            if find_word == '':
                find_word = message.text
                bot.send_message(message.chat.id, 'Отправьте слово на которое нужно поменять')
                bot.register_next_step_handler(message, edit_var)
            elif replace_word == "":
                replace_word = message.text
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('Все вхождения')
                item2 = types.KeyboardButton('Первое')
                item3 = types.KeyboardButton('Последнее')
                item4 = types.KeyboardButton('Другой вариант')
                markup.add(item1)
                markup.add(item2)
                markup.add(item3)
                markup.add(item4)
                bot.send_message(message.chat.id, 'Выберите что нужно заменять', reply_markup=markup)
                bot.register_next_step_handler(message, edit_var)
            elif all_or_one == "":
                all_or_one = message.text
                if all_or_one == 'Все вхождения':
                    res = replace_text(text, find_word, replace_word)
                    if res != []:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Назад')
                        markup.add(item1)
                        file = open('test.txt', 'w')
                        file.write(res)
                        file.close()

                        file = open('test.txt', 'r')
                        bot.send_document(message.chat.id, file, reply_markup=markup)
                        file.close()
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, main)
                        red = False
                    else:
                        bot.send_message(message.chat.id, 'В тексте нет такого слова')
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                elif all_or_one == 'Первое':
                    res = replace_first_word(text, find_word, replace_word)
                    if res != []:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Назад')
                        markup.add(item1)
                        file = open('test.txt', 'w')
                        file.write(res)
                        file.close()

                        file = open('test.txt', 'r')
                        bot.send_document(message.chat.id, file, reply_markup=markup)
                        file.close()
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, main)
                        red = False
                    else:
                        bot.send_message(message.chat.id, 'В тексте нет такого слова')
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                elif all_or_one == 'Последнее':
                    res = replace_last_word(text, find_word, replace_word)
                    if res != []:
                        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                        item1 = types.KeyboardButton('Назад')
                        markup.add(item1)
                        file = open('test.txt', 'w')
                        file.write(res)
                        file.close()

                        file = open('test.txt', 'r')
                        bot.send_document(message.chat.id, file, reply_markup=markup)
                        file.close()
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                        bot.register_next_step_handler(message, main)
                        red = False
                    else:
                        bot.send_message(message.chat.id, 'В тексте нет такого слова')
                        text = ''
                        find_word = ''
                        replace_word = ''
                        all_or_one = ''
                        start_or_finish = ''
                        another_amount = ''
                elif all_or_one == 'Другой вариант':
                    bot.send_message(message.chat.id, 'Отправьте число - количество замен')
                    bot.register_next_step_handler(message, edit_var)
            elif another_amount == '' :
                if message.text.isdigit():
                    another_amount = int(message.text)
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('С начала')
                    item2 = types.KeyboardButton('С конца')
                    markup.add(item1)
                    markup.add(item2)
                    bot.send_message(message.chat.id, 'Откуда начинать замены', reply_markup=markup)
                    bot.register_next_step_handler(message, edit_var)
                elif message.text.isdigit() == False:
                    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                    item1 = types.KeyboardButton('Начать заново')
                    markup.add(item1)
                    bot.send_message(message.chat.id, 'Вы ввели не число', reply_markup=markup)
                    text = ''
                    find_word = ''
                    replace_word = ''
                    all_or_one = ''
                    bot.register_next_step_handler(message, edit)
            elif start_or_finish == '':
                    start_or_finish = message.text
                    if start_or_finish == 'С начала':
                        res = replace_first_word_amount(text, find_word, replace_word, another_amount)
                        if res != []:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Назад')
                            markup.add(item1)
                            file = open('test.txt', 'w')
                            file.write(res)
                            file.close()

                            file = open('test.txt', 'r')
                            bot.send_document(message.chat.id, file, reply_markup=markup)
                            file.close()
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                            bot.register_next_step_handler(message, main)
                            red = False
                        else:
                            bot.send_message(message.chat.id, 'В тексте нет такого слова')
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                    elif start_or_finish == 'С конца':
                        res = replace_last_word_amount(text, find_word, replace_word, another_amount)
                        if res != []:
                            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                            item1 = types.KeyboardButton('Назад')
                            markup.add(item1)
                            file = open('test.txt', 'w')
                            file.write(res)
                            file.close()

                            file = open('test.txt', 'r')
                            bot.send_document(message.chat.id, file, reply_markup=markup)
                            file.close()
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''
                            bot.register_next_step_handler(message, main)
                            red = False
                        else:
                            bot.send_message(message.chat.id, 'В тексте нет такого слова')
                            text = ''
                            find_word = ''
                            replace_word = ''
                            all_or_one = ''
                            start_or_finish = ''
                            another_amount = ''


def poss_var(message):
    global lang
    if message.text == 'en':
        lang = 'en'
        bot.send_message(message.chat.id, 'Введите текст который нужно преобразовать в голос')
        bot.register_next_step_handler(message, speech)
    if message.text == 'ru':
        lang = 'ru'
        bot.send_message(message.chat.id, 'Введите текст который нужно преобразовать в голос')
        bot.register_next_step_handler(message, speech)

def speech(message):
    msg = message.text
    text_to_speech(msg, lang=lang)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Начать заново")
    markup.add(item1)
    with open('text_to_speech.mp3', 'rb') as f:
        bot.send_audio(message.chat.id, f, reply_markup=markup)
        bot.register_next_step_handler(message, edit)

def wiki(message):
    if message.text != "Назад↪️":
        text = message.text
        resualt = search_wiki(text)
        markup = types.InlineKeyboardMarkup()
        for res in resualt:
            btn = types.InlineKeyboardButton(res, callback_data=res)
            markup.add(btn)
        bot.send_message(message.chat.id, "Вот что удалось найти: ", reply_markup=markup)
    else:
        possibilites(message)

@bot.message_handler(content_types=['document'])
def handle_file(message):
    global text_file
    global text
    global word
    if text_file == 'Отправить файл📄':
        file_id = message.document.file_id
        file_info = bot.get_file(file_id)
        file_url = f'https://api.telegram.org/file/bot{token}/{file_info.file_path}'

        # Скачиваем файл
        response = requests.get(file_url)
        if response.status_code == 200:
            # Прочитаем содержимое файла
            file_content = response.content
            if text == '':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('/Редактировать')
                markup.add(item1)
                text = file_content.decode('utf-8')
                all_texts.append(text + '\n')
                if red == False:
                    bot.send_message(message.chat.id,f'Отправьте слово которое нужно найти',reply_markup=markup)
                else:
                    bot.send_message(message.chat.id, 'Отправьте слово которое нужно заменить')
                    bot.register_next_step_handler(message, edit_var)


        else:
            bot.reply_to(message, "Не удалось скачать файл. Начните сначала")

@bot.message_handler(content_types=['voice'])
def get_voice(message):
    global text
    file = bot.get_file(message.voice.file_id)
    bytes = bot.download_file(file.file_path)
    with open('voice.ogg', 'wb') as f:
        f.write(bytes)
    text = speech_to_text()
    all_texts.append(text + '\n')
    bot.send_message(message.chat.id, text='Отправьте слово которое нужно найти')
    bot.register_next_step_handler(message, find_voice)

def find_voice(message):
    global word
    global text
    word = message.text
    res = finder(text, word, regist, accurate_search,edit_text, all_texts, many_files)
    if res != []:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Начать заново')
        markup.add(item1)
        amount = len(res)
        finish_res = [str(res[i - 1]) for i in range(1, len(res) + 1)]
        bot.send_message(message.chat.id,
                         f'Вот что удалось найти: \n {'\n'.join(finish_res)} \n Найдено предложений: {amount}',
                         reply_markup=markup)
        text = ''
        word = ''
        bot.register_next_step_handler(message, edit)


    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton('Начать заново')
        markup.add(item1)
        bot.send_message(message.chat.id, 'В тексте нет такого слова', reply_markup=markup)
        text = ''
        word = ''
        bot.register_next_step_handler(message, edit)

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    global text
    global now_balance
    global topup_balance
    if topup_balance == 0:
        # Получаем информацию о самой большой фотографии (обычно это последний элемент в списке)
        file_id = message.photo[-1].file_id

        # Получаем информацию о файле
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        # Скачиваем файл
        downloaded_file = bot.download_file(file_path)

        # Сохраняем файл на диск
        with open("photo.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        bot.reply_to(message, "Фото успешно сохранено!")

        text_list = text_recognition('photo.jpg')

        for i in text_list:
            text += i + ' '
        all_texts.append(text + '\n')
        bot.send_message(message.chat.id, 'Отправьте слово которое нужно найти')
        bot.register_next_step_handler(message, func_text)
    else:
        file_id = message.photo[-1].file_id

        file_info = bot.get_file(file_id)
        file_path = file_info.file_path

        downloaded_file = bot.download_file(file_path)

        with open("photo.jpg", 'wb') as new_file:
            new_file.write(downloaded_file)

        text_list = text_recognition('photo.jpg')

        for i in text_list:
            text += i + ' '
        if author_name in text and str(topup_balance) in text:
            conn = sqlite3.connect('database.sql')
            cursor = conn.cursor()
            new_balance = now_balance + topup_balance
            new_balance = float(new_balance)
            cursor.execute("UPDATE users SET balance = ? WHERE login = ?", (new_balance, name))
            # Фиксация изменений
            conn.commit()

            # Закрытие соединения с базой данных
            conn.close()
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Начать заново')
            markup.add(item1)
            now_balance = user_balance(name)
            topup_balance = 0
            bot.send_message(message.chat.id, f'Баланс пополнен!\n Текущий баланс: {now_balance}р', reply_markup=markup)
            bot.register_next_step_handler(message, edit)
        else:
            bot.send_message(message.chat.id, 'Вы сделали что-то неправильно')

bot.polling(non_stop=True)