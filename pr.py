import telebot  # импортируем модуль pyTelegramBotAPI
import conf     # импортируем наш секретный токен
import random
import markovify
from nltk.tokenize import sent_tokenize
from flask import Flask, request
import os


#WEBHOOK_URL_BASE = "https://{}:{}".format(conf.WEBHOOK_HOST, conf.WEBHOOK_PORT)
#WEBHOOK_URL_PATH = "/{}/".format(conf.TOKEN)
# telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'} #задаем прокси
telebot.apihelper.proxy = conf.PROXY
bot = telebot.TeleBot(conf.TOKEN)  # создаем экземпляр бота




# -*- coding: utf-8 -*-
import flask




#telebot.apihelper.proxy = {'https': 'socks5h://geek:socks@t.geekclass.ru:7777'}  # задаем прокси
#bot = telebot.TeleBot(conf.TOKEN, threaded=False)  # бесплатный аккаунт pythonanywhere запрещает работу с несколькими тредами

# удаляем предыдущие вебхуки, если они были
# bot.remove_webhook()
#
# # ставим новый вебхук = Слышь, если кто мне напишет, стукни сюда — url
# bot.set_webhook(url=WEBHOOK_URL_BASE + WEBHOOK_URL_PATH)
#
# app = flask.Flask(__name__)

#       # этот обработчик запускает функцию send_welcome, когда пользователь отправляет команды /start или /help
#       @ bot.message_handler(commands=['start', 'help'])
#
#
# def send_welcome(message):
#     bot.send_message(message.chat.id, "Здравствуйте! Это бот, который считает длину вашего сообщения.")
#
#
# @bot.message_handler(func=lambda m: True)  # этот обработчик реагирует все прочие сообщения
# def send_len(message):
#     bot.send_message(message.chat.id, 'В вашем сообщении {} символов.'.format(len(message.text)))
#
#
# # пустая главная страничка для проверки
# @app.route('/', methods=['GET', 'HEAD'])
# def index():
#     return 'ok'


# обрабатываем вызовы вебхука = функция, которая запускается, когда к нам постучался телеграм
# @app.route(WEBHOOK_URL_PATH, methods=['POST'])
# def webhook():
#     if flask.request.headers.get('content-type') == 'application/json':
#         json_string = flask.request.get_data().decode('utf-8')
#         update = telebot.types.Update.de_json(json_string)
#         bot.process_new_updates([update])
#         return ''
#     else:
#         flask.abort(403)
#bot.remove_webhook()
# bot.set_webhook(url='https://alyozet.pythonanywhere.com/')
#
# app = Flask(__name__)
#
# @app.route('/', methods=["POST"])
# def webhook():
#     bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
#     return "!", 200

with open('hp.txt', encoding='utf-8') as f:
    text = f.read()

sents = sent_tokenize(text)
m = markovify.Text(text)
#for i in range(5):
#    print(m.make_short_sentence(max_chars=100))

def b(x):
    if x == 0:
        c = 'быков'
    elif x == 1:
        c = 'бык'
    else:
        c = 'быка'
    return(c)

def cor(x):
    if x == 0:
        c = 'коров'
    elif x == 1:
        c = 'корова'
    else:
        c = 'коровы'
    return(c)

# этот обработчик запускает функцию send_welcome,
# когда пользователь отправляет команды /start или /help
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.send_message(message.chat.id,
                     "Здравствуйте! Это бот, который играет. Напишите что-нибудь!")


isRunning = False
word = '0000'

@bot.message_handler(commands=['cows'])
def start_handler(message):
    print('i work')
    global isRunning
    global word
    if not isRunning:
        a = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        random.shuffle(a)
        word = ''.join(a[:4])
        chat_id = message.chat.id
        text = message.text
        msg = bot.send_message(chat_id, 'Играем в быков и коров. Если надо напомнить правила, напиши слово "правила", если нет -- угадывай')
        bot.register_next_step_handler(msg, askAge) #askSource
        #isRunning = True

def askAge(message):
    global isRunning
    chat_id = message.chat.id
    ans = message.text
    if ans == 'правила' or ans == 'Правила':
        msg = bot.send_message(chat_id, 'я загадал четырехзначное число без повторов. ты угадываешь. Я называю количество быков, то есть правильных цифр на своем месте, и количество коров, то есть правильных цифр на других местах. Удачи. Если надоело скажи стоп')
        bot.register_next_step_handler(msg, askAge)  # askSource
        return
    if ans == 'стоп' or ans == 'Стоп':
        msg = bot.send_message(chat_id,
                               'ахахахха нет уж, играем дальше!!!')
        bot.register_next_step_handler(msg, askAge)  # askSource
        return
    if not (ans.isdigit() and len(ans) == 4):
        msg = bot.send_message(chat_id, 'это не четырехзначное число')
        bot.register_next_step_handler(msg, askAge) #askSource
        return
    sovp = ans[0] == ans[1] or ans[0] == ans[2] or ans[0] == ans[3] or ans[1] == ans[2] or ans[1] == ans[3] or ans[2] == ans[3]
    if sovp:
        msg = bot.send_message(chat_id, 'все цифры должны быть разные')
        bot.register_next_step_handler(msg, askAge) #askSource
        return
    bik = 0
    kor = 0
    for i in range(4):
        if ans[i] == word[i]:
            bik += 1
        for j in range(4):
            if ans[i] == word[j] and i != j:
                kor += 1
    if ans != word:
        otvet = str(bik)+ ' '+b(bik)+', '+ str(kor) + ' '+cor(kor)+'. Вы пока не угадали, давайте еще'
        msg = bot.send_message(chat_id, otvet)
        bot.register_next_step_handler(msg, askAge)  # askSource
        return
    msg = bot.send_message(chat_id, 'вы угадали, это было число ' + word)
    isRunning = False
    #bot.register_next_step_handler(msg, menu)


r = 0
isRunning1 = False
def interp(x):
    if x == 'Роулинг':
        i = 1
    elif x == 'Бот':
        i = 0
    else:
        i = int(x) % 2
    return(i)

@bot.message_handler(commands=['hp'])
def hp(message):
    global isRunning1
    global r
    print('imhere')
    if not isRunning1:
        print('im there')
        chat_id = message.chat.id
        text = message.text
        rules = 'Я даю предложение из ГП на украинском или предложение, которое придумал сам. Не судите строго, украинский у меня не родной, и вообще я бот. Лучше угадайте, чье это предложение. Напишите "Роулинг" или "Бот"'
        r = random.randint(0, len(sents))
        if r % 2 == 0:
            snt = m.make_short_sentence(max_chars=100)
        else:
            snt = sents[r]
        msg = bot.send_message(chat_id, rules+'\n'+snt)
        bot.register_next_step_handler(msg, gad) #askSource
        #isRunning1 = True

def gad(message):
    global isRunning1
    chat_id = message.chat.id
    text = message.text
    if text != 'Роулинг' and text != 'Бот':
        msg = bot.send_message(chat_id, 'Напишите "Роулинг" или "Бот".')
        bot.register_next_step_handler(msg, gad) #askSource
        return

    if interp(text) == interp(str(r)):
        otv = 'Вiрно!'
    else:
        otv = 'Невiрно! Ти зовсім нічого не розумієш в ГП!'
    msg = bot.send_message(chat_id, otv)
    isRunning1 = False


@bot.message_handler(func=lambda m: True)
def menu(message):
    bot.send_message(message.chat.id, 'привет! чтобы играть в быков и коров наберите /cows, чтобы играть в "ГП на украинском или марковская цепь" нажмите /hp')


if __name__ == '__main__':
    bot.polling(none_stop=True, timeout=200)

#if __name__ == '__main__':
#    import os
#    app.debug = True
#    port = int(os.environ.get("PORT", 5000))
#    app.run(host='0.0.0.0', port=port)