import telebot
import requests

# ТГ токен
with open("token", "r") as file:
    token = file.readline()

bot = telebot.TeleBot(token)

# API для курса валют
with open("API_url", "r") as file:
    API_URL = file.readline()

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

@bot.message_handler(commands=['exchangerate'])
def exchange_rate(message):
    response = requests.get(API_URL)
    data = response.json()
    quotes = data["quotes"]

    usd_to_eur = quotes.get("USDEUR", "N/A")
    usd_to_rub = quotes.get("USDRUB", "N/A")
    usd_to_aed = quotes.get("USDAED", "N/A")

    message_text = (
        "Курсы валют по отношению к 1 USD:\n\n"
        f"1 USD = {usd_to_eur} EUR\n"
        f"1 USD = {usd_to_rub} RUB\n"
        f"1 USD = 60.61 Primogems\n"
        f"1 USD = {usd_to_aed} AED"
    )

    bot.send_message(message.chat.id, message_text)

bot.polling(none_stop=True)