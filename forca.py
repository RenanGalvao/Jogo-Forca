#!python3
import os
import sys
import random
import time
import platform

MAX_MISTAKES = 6
WORD_LIST_FILE_PATH = 'word-list.txt'
GAME_DEBUG = False

messages = {
  'INTRO_QUESTION': 'Olá, qual o seu nome? ',
  'WELCOME': 'Olá, %s! Seja bem-vindo(a) ao jogo da Forca! 😁',
  'HINT': 'Sua palavra tem %d letras! 💡',
  'HINT_MISTAKEN': 'Você só pode errar %d vezes antes de acertar a palavra! 🚨',
  'PRESS_TO_CONTINUE': 'Pressione Enter para continuar... ',
  'CHOOSE_LETTER': '👉 Escolha uma letra: ',
  'CORRECT_LETTER': 'Woow! Essa letra existe na sua palavra! 🙌',
  'WRONG_LETTER': 'Essa letra não existe na sua palavra. ❌',
  'MISTAKEN_LETTERS': '❌ Letras Erradas:',
  'WIN': 'Parabéns, %s! Você acertou a palavra! 🎉',
  'LOSE': 'Poxa, %s! Você não conseguiu acertar a palavra. 😕', 
  'CORRECT_WORD': 'A palavra era %s!',
  'PLAY_AGAIN': 'Deseja jogar novamente? (S/N) ',
  'WARNING': '🚨 Você deve escolher apenas uma letra por vez! 🚨',
  'ALREADY_USED': '🚨 Letra já usada! 🚨',
  'BYE': 'Tchau'
}

game_running = True
new_game = True
first_round = True
player_name = ''
word_list = ['JUNIOR', 'SENIOR', 'NODEJS', 'PROGRAMADOR', 'JAVASCRIPT']
current_word = ''
mistaken_letters = []
correct_letters = []


def clear_terminal():
    if platform.system() == 'Windows':
        os.system('cls')
    else:
        os.system('clear')

def break_lines(lines=1):
    print('\n'*lines, end='')

def get_name():
    global player_name
    player_name = input(messages['INTRO_QUESTION'])

def load_word_list():
    global word_list
    if os.path.exists(WORD_LIST_FILE_PATH):
        f = open(WORD_LIST_FILE_PATH, 'r')
        word_list = f.read().split('\n')

def choose_word():
    global current_word
    random.seed(time.time())
    current_word = random.choice(word_list)

def is_game_won():
    for letter in current_word:
        if letter not in correct_letters:
            return False
    return True

def show_letters():
    for letter in current_word:
        if letter in correct_letters:
            print('%s ' % letter, end='')
        else:
            print('_ ', end='')

def get_letter():
    chosen_letter = input(messages['CHOOSE_LETTER'])
    if chosen_letter.isalpha() or chosen_letter == '-' and len(chosen_letter) == 1:
        return chosen_letter.upper()
    else:
        return ''

def show_warning():
    break_lines(2)
    print(messages['WARNING'])
    time.sleep(3)

def show_letter_already_used():
    break_lines(2)
    print(messages['ALREADY_USED'])
    time.sleep(1)

def show_bye_message():
    sys.stdout.write(messages['BYE'])
    sys.stdout.flush()
    for i in range(3):
        time.sleep(0.5)
        sys.stdout.write('.')
        sys.stdout.flush()
    time.sleep(0.5)
    break_lines()

def play_again():
    global new_game, game_running, first_round, correct_letters, mistaken_letters

    answer = input(messages['PLAY_AGAIN'])
    if answer.isalpha() and len(answer) == 1 and answer.upper() == 'S':
        new_game = True
        first_round = False
        correct_letters = []
        mistaken_letters = []
        clear_terminal()
    else:
        game_running = False
        clear_terminal()
        show_bye_message()

while game_running:
    if not player_name:
        clear_terminal()
        get_name()
        clear_terminal()
        print(messages['WELCOME'] % player_name)
        load_word_list()

    if new_game:
        choose_word()
        new_game = False

        if first_round:
            break_lines(2)
        print(messages['HINT'] % len(current_word))
        break_lines()
        input(messages['PRESS_TO_CONTINUE'])

    while len(mistaken_letters) <= MAX_MISTAKES and not is_game_won():
        clear_terminal()
        if GAME_DEBUG:
            print('DEBUG:', current_word)

        print(messages['HINT_MISTAKEN'] % MAX_MISTAKES)
        break_lines(2)
        show_letters()
        break_lines(2)

        if mistaken_letters:
            print(messages['MISTAKEN_LETTERS'], ', '.join(mistaken_letters))
            break_lines()
        
        chosen_letter = get_letter()
        if not chosen_letter:
            show_warning()
            continue
        elif chosen_letter in current_word:
            if chosen_letter in correct_letters:
                show_letter_already_used()
            else:
                correct_letters.append(chosen_letter)
                print(messages['CORRECT_LETTER'])
        else:
            if chosen_letter in mistaken_letters:
                show_letter_already_used()
            else:
                mistaken_letters.append(chosen_letter)
                print(messages['WRONG_LETTER'])

    clear_terminal()
    if is_game_won():
        print(messages['WIN'] % player_name)
        break_lines()
        print(messages['CORRECT_WORD'] % current_word)
        break_lines(2)
    else:
        print(messages['LOSE'] % player_name)
        break_lines()
        print(messages['CORRECT_WORD'] % current_word)
        break_lines(2)
    play_again()
