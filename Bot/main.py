import os

import telebot
from telebot import types
from dotenv import load_dotenv, find_dotenv

import sqlite3
import send



load_dotenv(find_dotenv());

bot = telebot.TeleBot(os.getenv('TOKEN'))

Name = None
Surname = None
Room = None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Чат-бот "Кампус" рад приветствовать тебя! Давай знакомиться! Как тебя зовут?' )
    bot.register_next_step_handler(message, user_name)

def user_name(message):
    global Name
    Name = message.text.strip()

    mess = f'Отлично, {Name}! Теперь введи свою фамилию.'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.register_next_step_handler(message, user_surname)

def user_surname(message):
    global Surname

    Surname = message.text.strip()
    mess = f'Осталось только узнать в какой комнате ты живешь.'
    bot.send_message(message.chat.id, mess, parse_mode='html')
    bot.register_next_step_handler(message, room_number)
def room_number(message):
    global Room

    try:
        Room = int(message.text.strip())
    except ValueError:
        bot.send_message(message.chat.id, text="Неверный формат, введите корректный номер комнаты:")
        bot.register_next_step_handler(message, room_number)
        return

    conn = sqlite3.connect('db.sql')
    cur = conn.cursor()

    cur.execute("INSERT INTO users (name, surname, room) VALUES ('%s', '%s', '%s')" % (Name, Surname, int(Room)))

    conn.commit()
    cur.close()
    conn.close()

    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn = types.KeyboardButton('Продолжить')
    markup.row(btn)
    bot.send_message(message.chat.id, 'Пользователь зарегистрирован!', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, menu)

def menu(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard = True)
    btn1 = types.KeyboardButton('Основная информация')
    btn2 = types.KeyboardButton('Оставить заявку')
    markup.row(btn1, btn2)
    btn3 = types.KeyboardButton('Контакты сотрудников')
    btn4 = types.KeyboardButton('Обратная связь')
    markup.row(btn3, btn4)
    a = message.text.strip()
    bot.send_message(message.chat.id, 'Чем могу помочь?', parse_mode='html', reply_markup=markup)
    bot.register_next_step_handler(message, menu_click)


@bot.message_handler(content_types=['text'])
def menu_click(message):
    if (message.text == "Контакты сотрудников"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Администрация")
        btn2 = types.KeyboardButton("Оперотряд")
        back = types.KeyboardButton("<= Назад")
        markup.add(btn1, btn2, back)
        bot.send_message(message.chat.id, text="Выберете нужные контакты", reply_markup=markup)

    elif (message.text == "Оперотряд"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton("<= Назад")
        markup.add(back)
        bot.send_message(message.chat.id, text="Контакты:****", reply_markup=markup)

    elif (message.text == "Администрация"):
        bot.send_message(message.chat.id, text="Администратор: Чомаева Людмила Казбековна\n +7(985)943-32-34(мобильный телефон) 8(495)954-14-28(городской телефон)")

    elif(message.text == "Основная информация"):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        btn1 = types.KeyboardButton("Заселение")
        btn2 = types.KeyboardButton("Регистрация")
        btn3 = types.KeyboardButton("Военно-учетный стол")
        btn4 = types.KeyboardButton("Поликлиника")
        back = types.KeyboardButton("<= Назад")
        markup.add(btn1, btn2, btn3, btn4, back)
        bot.send_message(message.chat.id, text="Выберете нужный пункт", reply_markup=markup)
        bot.register_next_step_handler(message, mainInfo)

    elif(message.text == "Оставить заявку"):
        send_app(message)
    elif(message.text == "Обратная связь"):
        sendFeed(message)
    elif(message.text == "<= Назад"):
        menu(message)

@bot.message_handler(content_types=['text'])
def mainInfo(message):
    if(message.text == "Заселение"):
        bot.send_message(message.chat.id, text = '<b>Перечень необходимых документов:</b>' \
           '\n1) Паспорт и его ксерокопия;\n' \
           '2) <a href= "https://misis.ru/files/-/b52197f14e50de8df778016f1ab1db21/soglasie.pdf"> согласие на заключение договора найма жилого помещения</a> (для несовершеннолетних);\n' \
           '3) военнообязанным необходимо предъявить военный билет либо приписное свидетельство;\n' \
           '4) <a href = "https://misis.ru/files/-/0ca492680b0d2a4cb8e545f1aa563c9e/zayavlenie.pdf"> заявление на предоставление места в общежитии</a>;\n' \
           '5) копия полиса ОМС или ДМС;\n' \
           '6) справка о состоянии здоровья, выданная лицензированными медицинскими учреждениями, подведомственными Минздраву России, об отсутствии противопоказаний для проживания в общежитии с обязательной отметкой о прохождении флюорографии, об отсутствии инфекционных заболеваний (туберкулез, ВИЧ, гепатит В) и сертификат прививок.', parse_mode='html')
        bot.send_message(message.chat.id, text = '<b>Важно!</b>\n' \
            'Студенты, которые не достигли совершеннолетнего возраста, обязаны подавать всю документацию в присутствии одного из своих законных представителей — родителей или опекунов. Законные представители должны иметь при себе документ, удостоверяющий их личность. Лучше, если это будет паспорт. Опекунам или попечителям помимо паспорта необходимо предъявить уполномоченному лицу бумаги, удостоверяющие права опеки или попечительства над несовершеннолетним лицом.', parse_mode='html')
        bot.send_message(message.chat.id, text='Чтобы почитать подробнее нажмите <a href="https://misis.ru/applicants/accommodation/zaselenievobsh_ezhitiepervokusn/neobhodimyedokumenty/">Сюда</a>', parse_mode='html')
        bot.register_next_step_handler(message, mainInfo)

    elif (message.text == "Регистрация"):
        bot.send_message(message.chat.id, text= '<b>Необходимые документы:\n</b> 1)копия договора\n 2)копия паспорта\n Получить регистрацию можно прямо в общежитии, обратившись в администрацию.', parse_mode='html')
        bot.register_next_step_handler(message, mainInfo)

    elif(message.text == "Поликлиника"):
        bot.send_message(message.chat.id, text='<b>Чтобы прикрепиться к поликлинике, вам понадобятся:</b>\n 1)Паспорт гражданина РФ или временное удостоверение личности\n2)полис ОМС (как переоформить его на московский смотрите далее)\n3) в случае изменения места жительства — документ, подтверждающий смену места жительства;', parse_mode='html')
        bot.send_message(message.chat.id, text='<b>Прикрепиться к поликлинике можно двумя способами:</b>\n 1)Онлайн на mos.ru (https://www.mos.ru/pgu/ru/services/link/2375/)\n 2) обратившись с пакетом документов лично в выбранную поликлинику', parse_mode='html')
        bot.register_next_step_handler(message, mainInfo)

    elif (message.text == "Военно-учетный стол"):
        bot.send_message(message.chat.id, text='Про военно-учеьный стол можно подробно узнать <a href="https://misis.ru/students/military-accounting-table/">здесь</a> ', parse_mode='html')
        bot.register_next_step_handler(message, mainInfo)

    elif (message.text == "<= Назад"):
        menu(message)

def send_app(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("<= Назад")
    markup.add(back)
    bot.send_message(message.chat.id, text="Опишите вашу проблему, <b>обязательно увказав ФИО, номер комнаты и вид неисправности.</b>", reply_markup=markup, parse_mode='html')
    bot.register_next_step_handler(message, send_problem)

@bot.message_handler(content_types=['text'])
def send_problem(message):
    if message.text == '<= Назад':
        menu(message)
    else:
        problem = message.text.strip()
        send.send_email("aasikasik@yandex.ru", f'Заявка в комнату {Room} от {Name} {Surname}', problem)
        send.send_email("zayavka-dk@yandex.ru", f'Заявка в комнату {Room} от {Name} {Surname}', problem)
        bot.send_message(message.chat.id, text="Заявка отправлена, в ближайшее время с вами свяжутся!")

        conn = sqlite3.connect('db.sql')
        cur = conn.cursor()

        cur.execute("SELECT id FROM users WHERE id > 0 and name = '%s' and surname = '%s' and room = '%s'" % (Name, Surname, Room))
        user_id = cur.fetchone()
        cur.execute("INSERT INTO applications (user_id, applic) VALUES ('%s', '%s')" % (user_id[0], problem))

        conn.commit()
        cur.close()
        conn.close()

        menu(message)


def sendFeed(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("<= Назад")
    markup.add(back)
    bot.send_message(message.chat.id, text="Будем очень рады получить обратную связь!", reply_markup=markup, parse_mode='html')
    bot.register_next_step_handler(message, sendFeedback)

@bot.message_handler(content_types=['text'])
def sendFeedback(message):
    if message.text == '<= Назад':
        menu(message)
    else:
        feedback = message.text.strip()
        send.send_email("aasikasik@yandex.ru", f'Обратная связь о  {Name} {Surname} комната {Room}', feedback)
        bot.send_message(message.chat.id, text="Спасибо за обратную связь!")
        menu(message)


@bot.message_handler()
def get_user_text(message):
    if message.text == "Hello":
        bot.send_message(message.chat.id, "И тебе привет!", parse_mode="html")
    else:
        bot.send_message(message.chat.id, "Я тебя не понимаю :(", parse_mode="html")


bot.polling(none_stop=True)