import random
import time

join_timer = 60
word = ''
used_words = []


def get_jumble():
    global word
    words = ['Apple', 'Apocalypse', 'cat', 'computer', 'bird', 'national']
    # words = ['furze', 'fuses', 'fusee', 'fused', 'fusel', 'fuser', 'fussy', 'gales', 'galls', 'gamba', 'gamer', 'gamin']
    word = random.choices(words)[0].upper()
    # if len(words) > 0 and len(used_words) == 0:
    #     words.remove(word)
    #     used_words.append(word) 
    # else:
    #     word = random.choices(used_words)[0].upper()
    #     used_words.remove(word)
    #     words.append(word)
    
    jumble = ' '.join(random.sample(word, len(word)))    
    jumbled = ''
    random_number = random.randrange(1, len(word))
    jumbled += word[0]+' '
    for i in range(1, len(word)):
        if i == random_number and len(word) > 4:
            jumbled += word[i]+' '
        else:
            jumbled += '_ '
    return f'🔤 {len(word)} letters: <b>{jumble}</b> \n 🤔 : <b>{" ".join(jumbled)}</b>'

def start_timer(sec):
    for i in range(sec, 0, -1):
        time.sleep(1)
        join_timer = i
        
    
