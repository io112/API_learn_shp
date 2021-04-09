import os
import random
from enum import IntEnum
from typing import Optional, List, Dict

from telebot import TeleBot
from telebot.types import Message, ReplyKeyboardMarkup, KeyboardButton

api_key = os.getenv('API_KEY', 'define me')

bot = TeleBot(api_key)


class Game:
    class IncomingResult(IntEnum):
        SUCCESS = 0
        NAME_NOT_IN_LIST = -1
        NAME_REPEATS = -2
        NAME_LETTER_INVALID = -3

    class GameDifficulty(IntEnum):
        NOT_SET = 0
        MIDDLE = 1
        HARD = 2

    MAX_USER_ERRORS = 3
    __cities = None

    def __init__(self) -> None:
        self.__bot_used_names = []
        self.__user_used_names = []
        self.difficulty = Game.GameDifficulty.NOT_SET
        self.user_errors = 0
        if not Game.__cities:
            Game.__load_cities()

    @staticmethod
    def __load_cities() -> None:
        Game.__cities = []
        with open('cities.txt', 'r', encoding='utf-8') as file:
            for line in file:
                line = line.strip().lower()
                if Game.__city_name_is_correct(line):
                    Game.__cities.append(line)

    @staticmethod
    def __city_name_is_correct(name: str) -> bool:
        return not name.endswith(')') and ' ' not in name

    def __add_bot_name(self, name: str) -> None:
        self.__bot_used_names.append(name)

    def __add_user_name(self, name: str) -> None:
        self.__user_used_names.append(name)

    def __process_resign(self) -> bool:
        if self.difficulty == Game.GameDifficulty.MIDDLE:
            value = random.randint(0, 100)
            return value <= len(self.__bot_used_names)
        return False

    def __get_next_bot_word(self, last_letter: str = 'a') -> Optional[str]:
        if self.__process_resign():
            return None
        name = random.choice(Game.__cities)
        while self.__check_name_not_repeat(name) and name[0] != last_letter:
            name = random.choice(Game.__cities)
        return name

    def __check_name_not_repeat(self, name: str) -> bool:
        return not (name in self.__bot_used_names and name in self.__user_used_names)

    @staticmethod
    def __get_last_letter(word: str) -> str:
        letter = word[-1]
        return letter if letter not in 'йьъ' else word[-2]

    def bot_word_incoming(self) -> Optional[str]:
        name = self.__get_next_bot_word(last_letter=self.get_last_user_letter())
        if name:
            self.__add_bot_name(name)
        return name

    def get_last_letter_in_list(self, data: List[str]) -> str:
        return '' if len(data) == 0 else self.__get_last_letter(data[-1])

    def get_last_bot_letter(self) -> str:
        return self.get_last_letter_in_list(self.__bot_used_names)

    def get_last_user_letter(self) -> str:
        return self.get_last_letter_in_list(self.__user_used_names)

    def user_word_incoming(self, name: str) -> IncomingResult:
        name = name.lower()
        if name not in Game.__cities:
            self.user_errors += 1
            return Game.IncomingResult.NAME_NOT_IN_LIST
        if not self.__check_name_not_repeat(name):
            self.user_errors += 1
            return Game.IncomingResult.NAME_REPEATS
        if not name.startswith(self.get_last_bot_letter()):
            self.user_errors += 1
            return Game.IncomingResult.NAME_LETTER_INVALID
        self.user_errors = 0
        self.__user_used_names.append(name)
        return Game.IncomingResult.SUCCESS


class GameStorage:
    data: Dict[int, Game] = {}

    @staticmethod
    def new_game(user_id: int) -> None:
        GameStorage.data[user_id] = Game()

    @staticmethod
    def end_game(user_id: int) -> None:
        del GameStorage.data[user_id]

    @staticmethod
    def get_game(user_id: int) -> Game:
        return GameStorage.data[user_id]

    @staticmethod
    def is_game_started(user_id: int) -> bool:
        return user_id in GameStorage.data

    @staticmethod
    def is_difficulty_set(user_id: int) -> bool:
        return GameStorage.data[user_id].difficulty != Game.GameDifficulty.NOT_SET

    @staticmethod
    def set_difficulty_middle(user_id: int) -> None:
        GameStorage.data[user_id].difficulty = Game.GameDifficulty.MIDDLE

    @staticmethod
    def set_difficulty_hard(user_id: int) -> None:
        GameStorage.data[user_id].difficulty = Game.GameDifficulty.HARD


@bot.message_handler(commands=['start', 'help'])
def start_handler(message: Message) -> None:
    bot.send_message(message.chat.id, 'CITY game bot. Wellcome.')
    bot.send_message(message.chat.id, '/newgame - запустить новую игру')
    bot.send_message(message.chat.id, '/endgame - остановить игру')


@bot.message_handler(commands=['newgame'])
def newgame_handler(message: Message) -> None:
    GameStorage.new_game(message.chat.id)
    keyboard = ReplyKeyboardMarkup(row_width=2)
    keyboard.row(
        KeyboardButton('/middle'),
        KeyboardButton('/hard')
    )
    bot.send_message(message.chat.id, 'Начинается новая игра. Укажите уровень сложности', reply_markup=keyboard)


@bot.message_handler(commands=['endgame'])
def endgame_handler(message: Message) -> None:
    if not GameStorage.is_game_started(message.chat.id):
        bot.send_message(message.chat.id, 'Вы ещё не начинали игру, чтобы её заканчивать. Введите /newgame для начала')
        return
    GameStorage.end_game(message.chat.id)
    bot.send_message(message.chat.id, 'Игра принудительно остановлена, вы проиграли')


@bot.message_handler(commands=['middle', 'hard'])
def difficulty_handler(message: Message) -> None:
    if not GameStorage.is_game_started(message.chat.id):
        bot.send_message(message.chat.id, 'Ошибка, игра ещё не начинается. Введите /newgame для начала')
        return
    if GameStorage.is_difficulty_set(message.chat.id):
        bot.send_message(
            message.chat.id,
            'Ошибка, уровень сложности уже установлен. Вы не можете его изменить, пока не начнётся следующая игра.'
        )
        return
    if message.text == '/middle':
        GameStorage.set_difficulty_middle(message.chat.id)
        bot.send_message(message.chat.id, 'Установлен средний уровень сложности')
    if message.text == '/hard':
        GameStorage.set_difficulty_hard(message.chat.id)
        bot.send_message(message.chat.id, 'Установлен высокий уровень сложности')
    bot.send_message(message.chat.id, 'Приглашаю вас ввести первое название города', reply_markup=ReplyKeyboardRemove())


@bot.message_handler(content_types=['text'])
def text_handler(message: Message) -> None:
    if not GameStorage.is_game_started(message.chat.id):
        bot.send_message(message.chat.id, 'Ошибка, игра ещё не началась. Введите /newgame для начала')
        return

    if not GameStorage.is_difficulty_set(message.chat.id):
        bot.send_message(
            message.chat.id,
            'Ошибка, вы не установили уровень сложности. Установите его командами /middle или /hard.'
        )
        return

    game = GameStorage.get_game(message.chat.id)
    incoming_result = game.user_word_incoming(message.text)
    if incoming_result == Game.IncomingResult.NAME_NOT_IN_LIST:
        bot.reply_to(
            message,
            f'Я не знаю такого города. Текущее количество ошибок: ({game.user_errors}/{game.MAX_USER_ERRORS})'
        )
    if incoming_result == Game.IncomingResult.NAME_REPEATS:
        bot.send_message(
            message.chat.id,
            f'Ой, это имя уже было. Текущее количество ошибок: ({game.user_errors}/{game.MAX_USER_ERRORS})'
        )
    if incoming_result == Game.IncomingResult.NAME_LETTER_INVALID:
        bot.send_message(
            message.chat.id,
            f'Это имя не начинается на букву \'{game.get_last_bot_letter()}\'. '
            f'Текущее количество ошибок: ({game.user_errors}/{game.MAX_USER_ERRORS})'
        )
    if incoming_result in [-1, -2, -3] and game.user_errors == game.MAX_USER_ERRORS:
        GameStorage.end_game(message.chat.id)
        bot.send_message(message.chat.id, 'Увы, но игра окончена, вы проиграли =(')
    if incoming_result == Game.IncomingResult.SUCCESS:
        bot.send_message(
            message.chat.id,
            f'Название города корректное. '
            f'Теперь бот ищет название на букву \'{game.get_last_user_letter()}\''
        )
        name = game.bot_word_incoming().capitalize()
        if name:
            bot.send_message(
                message.chat.id,
                f'{name}. Вам нужно найти название, начинающееся на букву \'{game.get_last_bot_letter()}\''
            )
        else:
            GameStorage.end_game(message.chat.id)
            bot.send_message(message.chat.id, 'Бот не смог придумать подходящее название города. ')
            bot.send_message(message.chat.id, 'Игра окончена, вы выиграли!')


if __name__ == '__main__':
    bot.polling(none_stop=True)
