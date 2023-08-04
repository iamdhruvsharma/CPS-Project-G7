import telebot

bot_token = ''

bot = telebot.TeleBot(bot_token)

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = 
    bot.send_message(chat_id, "Hello")

bot.polling()

