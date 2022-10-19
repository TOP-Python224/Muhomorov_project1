"""Дополнительный модуль: глобальные переменные и константы."""


# глобальные переменные данных
STATS = {}
SAVES = {}

PLAYERS = ['PlayerA', 'PlayerB']
TOKENS = ('X', 'O')

DIM = 3
RANGE = range(DIM)
RANGE_FLAT = range(DIM**2)

TURNS = []
BOARD = [''] * DIM**2

PLAYERS_FILE = './players.ini'
SAVES_FILE = './saves.ini'

# глобальные константы
APP_TITLE = "КРЕСТИКИ-НОЛИКИ"
PROMPT = ' > '
