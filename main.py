import telebot
from telebot import types

# Чтоб никто не стащил >:(
with open("token", "r") as file:
    token = file.readline()

bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        f"{message.from_user.first_name}, данный бот сделан для лабы.")

@bot.message_handler(commands=['free'])
def free(message):
    bot.send_message(
        message.chat.id,
        "[Бесплатные деньги тут](https://vk.cc/8U7VuC)",
        parse_mode="Markdown"
    )

@bot.message_handler(commands=['convert'])
def convert(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('RUB', callback_data='convert_rub'))
    markup.add(types.InlineKeyboardButton('EUR', callback_data='convert_eur'))
    markup.add(types.InlineKeyboardButton('USD', callback_data='convert_usd'))

    bot.send_message(
        message.chat.id,
        "Выберите валюту ИЗ которой переводить:",
        reply_markup=markup
    )
@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'convert_rub':
        bot.send_message(callback.message.chat.id, "Вы выбрали RUB.")
    elif callback.data == 'convert_eur':
        bot.send_message(callback.message.chat.id, "Вы выбрали EUR.")
    elif callback.data == 'convert_usd':
        bot.send_message(callback.message.chat.id, "Вы выбрали USD.")
    else:
        bot.send_message(callback.message.chat.id, "Неизвестная валюта.")

bot.polling(none_stop=True)