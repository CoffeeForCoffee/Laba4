import telebot
import requests

# ТГ токен
with open("token", "r") as file:
    token = file.readline()

bot = telebot.TeleBot(token)

# API для курса валют
with open("API_url", "r") as file:
    API_URL = file.readline()

# Доступные валюты
currencies = {
    'USD': 'USD',
    'EUR': 'USDEUR',
    'RUB': 'USDRUB',
    'AED': 'USDAED',
    'GBP': 'USDGBP',
    'JPY': 'USDJPY',
    'CNY': 'USDCNY'
}

# Стартовое сообщение при запуске бота
@bot.message_handler(commands=['start'])
def main(message):
    bot.send_message(
        message.chat.id,
        f"{message.from_user.first_name}, данный бот сделан для лабы.")

# Бесплатные деньги
@bot.message_handler(commands=['free'])
def free(message):
    bot.send_message(
        message.chat.id,
        "[Бесплатные деньги тут](https://vk.cc/8U7VuC)",
        parse_mode="Markdown"
    )

# Курс валют
def get_exchange_rate():
    response = requests.get(API_URL)
    data = response.json()
    return data["quotes"]

# Курс валют через API
@bot.message_handler(commands=['exchangerate'])
def exchange_rate(message):
    quotes = get_exchange_rate()

    # Получаем инфу 1 USD к другим валютам
    usd_to_eur = quotes.get("USDEUR")
    usd_to_rub = quotes.get("USDRUB")
    usd_to_aed = quotes.get("USDAED")
    usd_to_gbt = quotes.get("USDGBP")
    usd_to_jpy = quotes.get("USDJPY")
    usd_to_cny = quotes.get("USDCNY")

    message_text = (
        "Курсы валют по отношению к 1 USD:\n\n"
        f"1 USD = {usd_to_eur:.2f} EUR\n"
        f"1 USD = {usd_to_rub:.2f} RUB\n"
        f"1 USD = 60.61 Primogems\n"
        f"1 USD = {usd_to_aed:.2f} AED\n"
        f"1 USD = {usd_to_gbt:.2f} GBT\n"
        f"1 USD = {usd_to_jpy:.2f} JPY\n"
        f"1 USD = {usd_to_cny:.2f} CNY\n"
    )

    bot.send_message(message.chat.id, message_text)

# Калькулятор
@bot.message_handler(commands=['calculate'])
def calculate(message):
    bot.send_message(message.chat.id,"Введите количество валюты:",)
    bot.register_next_step_handler(message, get_amount) # Переходим на следующий шаг

# Количество
def get_amount(message):
    try:
        amount = float(message.text)
        if amount <= 0:
            bot.send_message(message.chat.id, "Количество валюты должно быть больше 0. Попробуйте снова.")
            bot.register_next_step_handler(message, get_amount)
        else:
            bot.send_message(message.chat.id, "Введите название валюты, из которой переводите (например, EUR, RUB):")
            bot.register_next_step_handler(message, get_from_currency, amount)
    except ValueError:
        bot.send_message(message.chat.id, "Неверное количество валюты. Попробуйте снова.")
        bot.register_next_step_handler(message, get_amount)

# Названия валюты
def get_from_currency(message, amount):
    from_currency = message.text.upper()
    if from_currency in currencies:
        bot.send_message(message.chat.id, "Введите название валюты, в которую хотите перевести (например, EUR, RUB):")
        bot.register_next_step_handler(message, get_to_currency, amount, from_currency)
    else:
        bot.send_message(message.chat.id, "Неизвестная валюта. Попробуйте снова.")
        bot.register_next_step_handler(message, get_from_currency, amount)

# В другую валюту
def get_to_currency(message, amount, from_currency):
    to_currency = message.text.upper()
    if to_currency in currencies:
        quotes = get_exchange_rate()

        from_rate = quotes.get(f"USD{from_currency}", 1)
        to_rate = quotes.get(f"USD{to_currency}", 1)

        converted_amount = (amount / from_rate) * to_rate

        bot.send_message(
            message.chat.id,
            f"{amount} {from_currency} = {converted_amount:.2f} {to_currency}"
        )
    else:
        bot.send_message(message.chat.id, "Неизвестная валюта. Попробуйте снова (например, EUR, RUB).")
        bot.register_next_step_handler(message, get_to_currency, amount, from_currency)

bot.polling(none_stop=True)