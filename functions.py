"""Дополнительный модуль: вспомогательные функции."""

from configparser import ConfigParser
from data import *
board = list(' ' * DIM ** 2)


def read_ini() -> None:
    """Читает данные из ini-файла в глобальную переменную данных."""
    players = ConfigParser()
    players.read(PLAYERS_FILE, encoding='utf-8')
    for section in players.sections():
        STATS[section] = {
            key: int(value)
            for key, value in players[section].items()
        }
    saves = ConfigParser()
    saves.read(SAVES_FILE, encoding='utf-8')
    for section in saves.sections():
        players = section.split(';')
        players_key = (players[0], players[1])
        turns = [int(i) for i in saves[section]['turns'].split(',')]
        SAVES[players_key] = {players[0]: [], players[1]: [], 'turns': turns}
        for i, turn in enumerate(turns):
            SAVES[players_key][players[i % 2]].append(turn)

    print(SAVES)


def write_ini() -> None:
    """Записывает данные из глобальной переменной данных в ini-файл."""
    players = ConfigParser()
    players.read_dict(STATS)
    with open(PLAYERS_FILE, 'w', encoding='utf-8') as ini_file:
        players.write(ini_file)
    saves = ConfigParser()
    for elems in SAVES.keys():
        player1, player2 = list(elems)
        section = f"{player1};{player2}"
        saves[section] = {}
        saves[section]['turns'] = ','.join([str(i) for i in SAVES[elems]['turns']])
    with open('saves_test.ini', 'w', encoding='utf-8') as ini_file:
        saves.write(ini_file)


def draw_board(align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""


if __name__ == '__main__':
    # pass
    read_ini()
    write_ini()
    # print(STATS)
    # STATS['Player1']['wins'] = 3
    # STATS['Player2']['fails'] = 1
    # STATS['Ioann'] = {'wins': 0, 'fails': 0, 'ties': 0}
    # write_ini()
    # read_ini()
    # print(STATS)
    # print(SAVES)
