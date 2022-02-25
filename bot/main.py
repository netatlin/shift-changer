import telebot
from telebot import types
import random
import logging
from json_formatter import JSONFormatter
from config import TOKEN


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
loggingStreamHandler = logging.StreamHandler()
loggingStreamHandler.setFormatter(JSONFormatter())
logger.addHandler(loggingStreamHandler)
logger.info({"message": 'Bot is starting'})

bot = telebot.TeleBot(TOKEN)
channel_id = -1001639740273

random_message = lambda message: random.choice(message)

random_filling_message = lambda filling, message: random.choice(message) % filling

# Приветственное сообщение
first_message = ['Привет! Я — бот для поиска замен в нашей прекрасной Кухне на Районе. Прочитай, пожалуйста, внимательно, '
                  'как мною пользоваться, чтобы всем было удобно.\n\nЕсли тебе нужно найти себе замену, напиши мне '
                  'подробно, на какое число ищешь, на какой день недели и с какого по какой час. И добавь комментарий, '
                  'если нужно. Например: \n\n<i>«Всем хай! Ищу героя на 12 мая, среда, с 12:00 до 17:00. '
                  'У меня экз — могу вернуться пораньше, и тогда тыкну, как заберу смену обратно 🙌🏻‎»</i> '
                  '\n\nЕсли что-то пойдёт не так, или если нужно будет отозвать твоё сообщение, всегда по всем '
                 'вопросам работы бота и канала пиши Яне: @lilgorchitca'
                 ]

# Сообщение в ответ на сообщение
reply_message = ['Готово, ищи себя в канале замен! Как только твой спаситель найдётся, напишу тебе. '
                 'Поэтому советую меня не мьютить ;)',
                 'Супер! Уже отправил твоё сообщение в канал. Напишу, если найдётся человек на замену. Не мьють меня!',
                 'Ого! Сообщение уже переслано в канал. Жди, когда тебе придут на подмогу. Уверен, это '
                 'обязательно случится! Как только кто-то откликнется – я тебе сообщу',
                 'Сообщение отличное, у тебя очень красивый почерк. Я отправил его в канал замен, там им тоже '
                 'любоваться будут. А кому-то так понравится, что он даже выйдет за тебя! (на смену) \n\n(извиняюсь за '
                 'шутку, я когда это писал, был в очень хорошем настроении)',
                 'Блин, это же надо так! Так красиво сформулировать свои мысли! Ты не книги случайно пишешь? В любом '
                 'случае, спасибо. Вообще, такие люди как ты помогают мне осознавать, что то, что я делаю – '
                 'важно. Вот, уже переслал твоё сообщение в канал. Остаётся только надеяться и ждать, что '
                 'тебе кто-то ответит. Я напишу тебе! Как только – так сразу! Обещаю!']

# Название для героя
hero_nick = ['Герой', 'Спаситель', 'Лучший человек на земле', 'Замечательнейший человек', 'Лучшим в этот раз оказался',
             'Идеальный человек', 'Дорогой наш человечек', 'Золотце кухни']

# Надписи для кнопок
buttons = ['Забираю', 'Выйти на смену', 'Стать героем', 'Помочь нуждающемуся', 'Спасти ситуацию']

# Начало сообщения после нажатия на кнопку
after_button_message_top = ['Привет! Как-то раз от тебя пришло сообщение', 'Ого! Однажды ты написал мне',
                            'До сих пор вспоминаю твоё последнее сообщение. Как там было? Что то вроде',
                            'Помнишь меня? Я бот! Тот самый, что помогает найти замену. Так вот, ты писал',
                            'Я же обещал тебе, что напишу! Вот – пишу! Не помнишь? Ну погоди, ты же писал мне']
# Конец сообщения после нажатия на кнопку
after_button_message_bottom = ['Хорошие новости! Тебе поможет @%s! Скорее спишись с ним, поблагодари и '
                               'не забудь поставить в известность своего лидера. Нужная ссылка на его тг ниже, '
                               'чтобы тебе долго не ходить',
                               'В общем. Некто @%s вызвался тебе помочь, представляешь! '
                               'Пиши ему, скажи там "спасибо" и всё такое. А также не забудь поставить в известность '
                               'своего лидера. Нужная ссылка на его тг ниже, '
                               'чтобы тебе долго не ходить',
                               'Так вот! Замена наконец-то найдена. Лучшим человеком оказался @%s. Круто, да? '
                               'Свяжись с ним, поблагодари, обязательно отправь стикер (я реально проверяю, без стикера '
                               'больше не сможешь замены искать). А ещё не забудь поставить в известность '
                               'своего лидера. Нужная ссылка на его тг ниже '
                               ]

# Список лидеров
leaders = '@lilgorchitca\n@ravenkroft\n@laterdi'

@bot.message_handler(commands=['start'])
def start_message(message):
    """Логика при запуске бота"""
    reply_text = random_message(first_message)
    bot.send_message(message.chat.id, reply_text, parse_mode="HTML")


@bot.message_handler()
def my_orders_message(message):
    """Логика при отправке сообщения в бота"""
    keyboard = types.InlineKeyboardMarkup()
    button_text = random_message(buttons)
    callback_button = types.InlineKeyboardButton(text=button_text, callback_data=message.chat.id)
    keyboard.add(callback_button)
    reply_text = random_message(reply_message)

    # Отправляет сообщение в канал
    bot.copy_message(channel_id, message.chat.id, message.id, reply_markup=keyboard)

    # Отправляет ответку автору сообщения
    bot.send_message(message.chat.id, reply_text, reply_to_message_id=message.id)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    """Логика при нажатии на кнопку"""
    if call.message:
        hero = call.from_user.username
        hero_nickname = random_message(hero_nick)
        new_text = call.message.text + f'\n\n<b>{hero_nickname}: @{hero}</b>'

        # Обновляет сообщение
        bot.edit_message_text(chat_id=channel_id, message_id=call.message.message_id, text=new_text, parse_mode="HTML")

        after_top = random_message(after_button_message_top)
        after_bottom = random_filling_message(hero, after_button_message_bottom)
        after_text = f'{after_top}: \n\n<i>{call.message.text}</i>\n\n{after_bottom}\n\n{leaders}'

        # Отправляет сообщение автору сообщения в канале
        bot.send_message(call.data, text=after_text, parse_mode="HTML")


bot.polling(none_stop=True)
