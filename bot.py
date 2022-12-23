import telebot
from telebot.types import Message
from telebot import types

# dev
import config
import common


lastMessageId, lastChatId = 0, 0


def go_terms(form, message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
            telebot.types.InlineKeyboardButton('Join the Group', url='https://t.me/+0aP2XjKFmM1hZDdl')        
    )
    if form == 'tel-term-vid' or form == 'tel-term-txt':
        if form == 'tel-term-vid':
            bot.send_message(
                message.chat.id,
                'https://www.youtube.com/watch?v=fHI8X4OXluQ',
                reply_markup=keyboard,
                # parse_mode='HTML'
            )
        else:
            bot.send_message(message.chat.id, 'rules in telugu')
    elif form == 'eng-term-vid' or form == 'eng-term-txt':
        if form == 'eng-term-vid':
            bot.send_message(
                message.chat.id,
                'https://www.youtube.com/watch?v=fHI8X4OXluQ',
                reply_markup=keyboard,
                # parse_mode='HTML'
            )
        else:
            bot.send_message(message.chat.id, 'rules in english')
    

def go_lang(lang, message):
    bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup()
    if lang == 'lang-eng':
        keyboard.row(
            telebot.types.InlineKeyboardButton('Video', callback_data='eng-term-vid'),
            telebot.types.InlineKeyboardButton('Read', callback_data='eng-term-txt')
        )
        bot.send_message(
            message.chat.id, 'Welcome! ( Watch a video or Read )',
            reply_markup=keyboard,
        )
    elif lang == 'lang-tel':
        keyboard.row(
            telebot.types.InlineKeyboardButton('Video (వీడియో)', callback_data='tel-term-vid'),
            telebot.types.InlineKeyboardButton('Read (చదవండి)', callback_data='tel-term-txt')
        )
        bot.send_message(
            message.chat.id, 'స్వాగతం! (వీడియో చూడండి లేదా చదవండి)',
            reply_markup=keyboard,
        )
   

def go_games(query, message):
    # bot.send_chat_action(message.chat.id, 'typing')
    bot.delete_message(message.chat.id, message.id)
    keyboard = telebot.types.InlineKeyboardMarkup()
    if query == 'game-jumble':
        keyboard.row(
            telebot.types.InlineKeyboardButton('create game', callback_data='create-game-jumble'),
        )
        bot.send_message(
            message.chat.id, 'create a game now ',
            reply_markup=keyboard,
        )
    elif query == 'game-guess':
        bot.send_message(
            message.chat.id, 'Guess the word coming soon...',
        )
        

def create_game(game, message, condition = True):
    jumbled = common.get_jumble()
    if (game == 'create-game-jumble'):
        if condition:
            bot.delete_message(message.chat.id, message.id)
        bot.send_message(
                message.chat.id, f'The word is : \n <b>{jumbled}</b>',
                parse_mode='HTML'
            )
    
         
def what_is_language(lang, query):
#    bot.answer_callback_query(query.id)
   go_lang(lang, query.message)

def what_is_terms(form, query):
    # bot.answer_callback_query(query.id)
    go_terms(form, query.message)

def what_is_game(query, option):
    go_games(query, option.message)

def create_a_game(game, option):
    create_game(game, option.message)
    
print("Hi, I'm bot!")
bot = telebot.TeleBot(config.API_KEY)

def main():
    @bot.message_handler(commands=['start', 'games', 'help'])
    def send_welcome(message):
        global lastMessageId, lastChatId
        command = message.text
        keyboard = telebot.types.InlineKeyboardMarkup()
        if command == '/start':
            keyboard.row(
                telebot.types.InlineKeyboardButton('English', callback_data='lang-eng'),
                telebot.types.InlineKeyboardButton('Telugu (తెలుగు)', callback_data='lang-tel')
            )
            bot.send_message(message.chat.id, 
                f"Hollo {message.from_user.first_name}, \n"
                'To get all the available options press <b>/help</b> \n' +
                'Choose you language ( భాష ) :',
                reply_markup=keyboard,
            )
            
        elif command == '/help':
            bot.send_message(message.chat.id, 'Sorry! Help is not available')
            
        ## Jumbled word game section
        elif command == '/games':
            # print(message)
            keyboard.row(
                telebot.types.InlineKeyboardButton('Jumble Word', callback_data='game-jumble'),
                telebot.types.InlineKeyboardButton('Guess the Word', callback_data='game-guess'),
            )
            bot.send_message(message.chat.id, 
                f"Hollo {message.from_user.first_name}, \n"
                'Choose a game :',
                reply_markup=keyboard,
            )
        
    @bot.message_handler(content_types='text')
    def send_welcome(message):
        msg = message.text
        if (msg.upper() == common.word):
            # bot.send_message(message.chat.id, 'Congrats! you win :)')
            create_game('create-game-jumble', message, False)
            


    @bot.callback_query_handler(func=lambda call: True)
    def lang_setter(option):
        query = option.data
        # print(option)
        if query.startswith('lang-'):
            what_is_language(query, option)
        elif '-term-' in query:
            what_is_terms(query, option)
        elif query.startswith('game-'):
            # bot.delete_message(option.message.chat.id, option.message.id)
            what_is_game(query, option)
        elif query.startswith('create-game-'):
            # bot.delete_message(option.message.chat.id, option.message.id)
            create_a_game(query, option)
        
    
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()