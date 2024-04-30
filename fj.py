import telebot
from googletrans import Translator, LANGUAGES
from telebot import types

# Замените 'YOUR_TOKEN_HERE' на токен вашего бота
bot_token = "7016437123:AAG6fgKS4JcXlLzIMUtRl6bitLPN5Q59BzM"
bot = telebot.TeleBot(bot_token)

translator = Translator()

# Список языков для перевода (можно добавить или изменить)
languages = {
    'english': 'en',
    'spanish': 'es',
    'french': 'fr',
    'german': 'de',
    'russian': 'ru',
    'italian': 'it',
    'portuguese': 'pt',
    'chinese': 'zh-cn',
    'japanese': 'ja',
    'korean': 'ko'
}


def generate_markup():
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for lang in languages.keys():
        markup.add(types.KeyboardButton(lang.capitalize()))
    return markup


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Привет! Отправьте мне текст, и выберите язык для перевода.")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    markup = generate_markup()
    msg = bot.reply_to(message, "Выберите язык для перевода:", reply_markup=markup)
    bot.register_next_step_handler(msg, process_translation_step, message.text)


def process_translation_step(message, text_to_translate):
    language = message.text.lower()
    if language in languages:
        try:
            translated = translator.translate(text_to_translate, dest=languages[language])
            reply_text = f"Перевод на {language}: {translated.text}\nОбращайтесь)"
        except Exception as e:
            reply_text = f"Ошибка перевода: {str(e)}"
    else:
        reply_text = "Извините, я не поддерживаю этот язык."

    bot.send_message(message.chat.id, reply_text, reply_markup=types.ReplyKeyboardRemove())


if __name__ == '__main__':
    bot.polling()
