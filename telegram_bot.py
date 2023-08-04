import telebot

bot_token = '5809770346:AAGA2sLrBDyzMY4Fq2rR3o6YkHv2U9l-OCk'

bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    print("chat ", chat_id)

bot.polling()

chat_id = 5980789960
