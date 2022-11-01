"""Дополнительный модуль: глобальные переменные и константы."""

# импорт из стандартной библиотеки
from numbers import Real
from typing import Sequence


# глобальные переменные данных
STATS = {}
SAVES = {}

PLAYERS = []
TOKENS = ('X', 'O')

WEIGHT_OWN = 1.5
WEIGHT_FOE = 1

BOT_LEVEL = 0

DIM = 3
CELLS = DIM**2
RANGE = range(DIM)
ALL_TURNS = range(1, CELLS+1)

TURNS = []
BOARD = ['']*CELLS

BOT_SM = ()

TRAINING = False


# глобальные переменные типов для аннотаций
Series = Sequence[Real | str]
Matrix = Sequence[Series]
Score = tuple[dict, dict]


# глобальные константы
APP_TITLE = "КРЕСТИКИ-НОЛИКИ"
PROMPT = ' > '

COMMANDS = {
    'новый игрок': ('player', 'игрок', 'p', 'н'),
    # ИСПРАВИТЬ: и какая же команда будет выбрана по вводу 'и'?
    'начать новую партию': ('new', 'игра', 'n', 'и'),
    'восстановить игру': ('load', 'загрузка', 'l', 'з'),
    'отобразить результаты': ('stats', 'таблица', 's', 'т'),
    'включить режим обучения': ('tutorial', 'обучение', 't', 'о'),
    'изменить размер поля': ('dim', 'размер', 'd', 'р'),
    'выйти из игры': ('quit', 'выход', 'q', 'в')
}
