"""Дополнительный модуль: глобальные переменные и константы."""

# импорт из стандартной библиотеки
from numbers import Real
from typing import Sequence
from random import choice

# глобальные переменные данных
STATS = {}
SAVES = {}

PLAYERS = []
TOKENS = ('X', 'O')
WEIGHT_OWN = 1.5
WEIGHT_FOE = 1
BOT_LEVEL = 0

DIM = 3
RANGE = range(DIM)
RANGE_FLAT = range(DIM**2)

TURNS = []
BOARD = [''] * DIM**2
# BOARD = [choice(TOKENS) for i in range(25)]
TRAINING = False

# глобальные переменные типов для аннотаций
Series = Sequence[Real | str]
Matrix = Sequence[Series]
Score = tuple[dict, dict]

# глобальные константы
APP_TITLE = "КРЕСТИКИ-НОЛИКИ"
PROMPT = ' > '

COMMANDS = {
    'новый игрок': ('player', 'игрок', 'p', 'и'),
    'начать новую партию': ('new', 'игра', 'n', 'и'),
    'восстановить игру': ('load', 'загрузка', 'l', 'з'),
    'отобразить результаты': ('table', 'таблица', 't', 'т'),
    'включить режим обучения': ('tutorial', 'обучение'),
    'выйти из игры': ('quit', 'выход', 'q', 'в')
}

