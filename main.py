import telebot
from config import TOKEN

time_delta = 60 * 60

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Вадик сука")

@bot.message_handler()
def my_orders_message(message):
    """Логика при отправке сообщения в бота"""
    bot.send_message(message.chat.id, 'Ты похоже что-то перепутал', reply_to_message_id=message.id)
    # 1. Получает сообщение
    # 2. Отправляет сообщение в канал

@bot.chat_member_handler()
def chat_update_handler(chat_member_updated):
    """Логика при нажатии кнопки на сообщении"""

    bot.send_message(137378, chat_member_updated)

    # 1. Получает нажатие кнопки
    # 2. Обновляет сообщение
    # 3. Отправляет сообщение автору сообщения в канале

bot.polling(none_stop=True)
