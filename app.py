import telebot
from config import *
from extensions import APIException, API

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Здравствуйте! \nЯ бот-конвертер валют и я могу:  \n1. Показать список доступных валют через команду /values \
    \n2. Вывести конвертацию валюты через команды:\n <имя валюты>\n <в какую валюту перевести>\n' \
    ' <количество переводимой валюты>\n команды необходимо вводить через пробел.\
      \n3. Напомнить, что я могу - через команду /help'
    bot.reply_to(message, text)


@bot.message_handler(commands=['help'])
def help(message: telebot.types.Message):
    text = '1.Чтобы начать конвертацию, введите команды боту в следующем формате: \n<имя валюты> <в какую валюту перевести> <количество переводимой валюты>.Команды необходимо вводить через пробел.' \
           '\n2.Чтобы увидеть список всех доступных валют, введите команду\n/values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def get_price(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIException('Введите правильную команду или 3 параметра (см./help)')

        quote, base, amount = values
        total_base = API.get_price(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Что-то пошло не так с {e}.Введите команды заново.')
    else:
        text = f'Переводим {quote} в {base}\n{amount} {base} = {total_base} {quote}'
        bot.send_message(message.chat.id, text)



bot.polling()