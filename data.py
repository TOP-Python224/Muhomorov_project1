"""Дополнительный модуль: глобальные переменные и константы."""


# глобальные переменные данных
STATS = {}
SAVES = {}

PLAYERS = []
TOKENS = ('X', 'O')

DIM = 3
RANGE = range(DIM)
RANGE_FLAT = range(DIM**2)

TURNS = []
BOARD = [' '] * DIM**2


# глобальные константы
APP_TITLE = "КРЕСТИКИ-НОЛИКИ"
PROMPT = ' > '
