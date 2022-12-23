import tab
import telebot
from telebot.types import Message
from telebot import types
import time, datetime,random
import threading,os
import common
import schema

from dotenv import load_dotenv
load_dotenv()

gameCounter = 1
new_data = []
participants = {}
Session_id = 0

game_time = datetime.datetime.now()

DB =  schema.DynamoDB_con()


def delete_message(chat_id, message_id, sec = 0):
    time.sleep(sec)
    bot.delete_message(chat_id, message_id)
    # return True
    
def alert(messageId, msg, show_alert= False):
    if show_alert:
        bot.answer_callback_query(messageId, msg, show_alert=True)
    else:
        bot.answer_callback_query(messageId, msg)

def go_games(query, message):
    # bot.send_chat_action(message.chat.id, 'typing')
    keyboard = telebot.types.InlineKeyboardMarkup()
    delete_message(message.chat.id, message.id)
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
    print(message.from_user.id, message.from_user.first_name, 'created jumble here ---')
    # chat_type = message.chat.types
    Session_id = random.randrange(10000,99999)
    print('se000000: ',Session_id)
    # print(message)
    # if chat_type == 'supergroup':
    # participants[message.from_user.id] ={
    #                     "Datetime": str(game_time),
    #                     "User_id": str(message.from_user.id),
    #                     "Points_Scored": 0
    #                 }
    new_data = {"JumbledWord_InitiatedByUser_ID": str(message.from_user.id),"datetime": str(game_time), 'JumbledWord_Participation':1}
    
    DB.sending(new_data,'JumbledWord_Engagement')

    global jumble_time_message
    keyboard = telebot.types.InlineKeyboardMarkup()
    print(message.message.chat.id, message.message.id)
    # return
    if (game == 'create-game-jumble'):
        keyboard.row(
            telebot.types.InlineKeyboardButton('🤝 Join Game', callback_data='join-jumble'),
        )
        # delete_message(message.message.chat.id, message.message.id)
        jumble_time_message = bot.send_message(
                chat_id, f'You Have  *⌛60* _s_ to Join',       
                reply_markup=keyboard,
                parse_mode='markdown'
            )
        for i in range(12, -1, -1):
            time.sleep(5)
            bot.edit_message_text(
                chat_id = message.message.chat.id, message_id = time_message.id, 
                text = f'Jumbled Word \n\n *⌛ 00m : {i*5}*_s_\n \n Click the Join Button to make count your participation \n\n"_After timer ends game will start automatically_"',
                reply_markup=keyboard,
                parse_mode='markdown'
            )
            join_timer = i*5
        print(join_timer, 'ff')

        
def join_game(game, message, condition = True):
    jumbled = common.get_jumble()
    keyboard = telebot.types.InlineKeyboardMarkup()
    if (game == 'join-jumble'):
        if join_timer == 0:
            keyboard.row(
                telebot.types.InlineKeyboardButton('💡 Hint ', callback_data='pass-jumble'),
                telebot.types.InlineKeyboardButton('❌ Quit', callback_data='quit-jumble'),
            )
            gameCounter += 1
            
        elif time < 10:
            print(60-common.join_timer, 's time left')
            # print(message, 'yyyy')
            alert(message.id, f'Your participation recorded successfully \nWait for the timer to end')
            
        elif gameCounter > 10:
            print(gameCounter, 'game left')
            common.time_breaker = False
            winner_announce = threading.Thread(target=common.start_timer, args=('ques-wait', 1, 'join-jumble', message))
            winner_announce.start()
                
            # threads = threading.Thread(target=db_operations.post_data, args=(participants, 'temp_session'))
            # threads.start()
            
            game_creater['total_participants'] = len(participants)
            print(game_creater, '67676767776')
            # creator = threading.Thread(target=db_operations.post_data, args=(game_creater, 'jumble_engagement'))
            # creator.start()
            # alert(message.id, f'10/10 word completed')
            
def winner(message, time = 20):
    common.word = ''
    print(participants)
    chat_id = message.json['chat']['id']
    if time == 20:
        bot.send_message(chat_id, '''
                    Thanks for Playing the Game! \nHere are the Winners :- \n\t \t *Name \t | \t Points* \n 🥇\t *Mahendra \t -8* \n 🥈\t *Prem \t 8* \n 🥉\t *Demo \t 5*
             ''',
        parse_mode='markdown'
        )
    
print("Hi, Jumble here!")
bot = telebot.TeleBot(os.getenv('API_KEY'))

def main():
    @bot.message_handler(commands=['start', 'games', 'help', 'check'])
    def send_welcome(message):
        command = message.text
        print(message.chat.type)
        keyboard = telebot.types.InlineKeyboardMarkup()   
        if command == '/help':
            bot.send_message(message.chat.id, 'Sorry! Help is not available')
            
        ## Jumbled word game section
        elif command.startswith('/games'):
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
        elif command.startswith('/check'):
            print(command)
        
    @bot.message_handler(content_types=['text'])
    def send_welcome(message):
        msg = message.text
        print(msg, common.word)
        keyboard = telebot.types.InlineKeyboardMarkup()
        
        if (msg.upper() == common.word):
            # bot.send_message(message.chat.id, 'Congrats! you win :)')
            join_game('join-jumble', message, False)
            


    @bot.callback_query_handler(func=lambda call: True)
    def callback_query(option):
        query = option.data
        old_data,newId = DB.reading('Temp_JumbledWord_Session')
        print(old_data)
        if query == 'join-jumble':
            while True:
                print(new_data)
                if newId not in participants:
                    participants[newId] ={
                            "Id":newId,
                            "Datetime": str(game_time),
                            "User_Id": str(option.from_user.id),
                            "Points_Scored": 0
                            "session_Id":
                        }
                    break
                else:
                    newId+=1
            print(participants)

            for dic in participants:
                print(dic,';;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;;')
                DB.sending(participants[dic],'Temp_JumbledWord_Session')
            
        elif query.startswith('pass-'):
            alert(option.id, 'What hint, do it your self...')
        elif query.startswith('quit-'):
            alert(option.id, 'This feature is in progress...')
            
        elif query.startswith('join-'):
            what_to_join(query, option)
                
        
    
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()