import telebot

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
def site(message):
    bot.send_message(
        message.chat.id,
        "[Бесплатные деньги тут](https://vk.cc/8U7VuC)",
        parse_mode="Markdown"
    )


bot.polling(none_stop=True)