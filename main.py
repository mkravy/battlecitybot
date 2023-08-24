import telebot

# создаем объект бота
bot = telebot.TeleBot('6341865034:AAHvb4vpFLO4b7jC0436bEnwR5IhbrT0EgQ')

# обработчик команды "/start"
@bot.message_handler(commands=['start'])
def start_handler(message):
    # создаем клавиатуру с кнопкой "Привет"
    keyboard = telebot.types.ReplyKeyboardMarkup()
    keyboard.row('Привет')
    # отправляем пользователю сообщение и клавиатуру
    bot.send_message(message.chat.id, 'Нажми на кнопку "Привет"', reply_markup=keyboard)

# обработчик нажатия на кнопку "Привет"
@bot.message_handler(func=lambda message: message.text == 'Привет')
def hello_handler(message):
    # отправляем пользователю сообщение "Здравствуй"
    bot.send_message(message.chat.id, 'Здравствуй')

# запускаем бота
bot.polling(none_stop=True)