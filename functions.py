"""Дополнительный модуль: вспомогательные функции."""

from configparser import ConfigParser
from data import *


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
        curr_section = {}
        turns = [int(i) for i in saves[section]['turns'].split(',')]
        players = section.split(';')
        curr_section[players[0]], curr_section[players[1]] = [], []
        for i, turn in enumerate(turns):
            curr_section[players[i % 2]].append(turn)
            curr_section['turns'] = turns
        SAVES.append(curr_section)
    print(SAVES)


def write_ini() -> None:
    """Записывает данные из глобальной переменной данных в ini-файл."""
    players = ConfigParser()
    players.read_dict(STATS)
    with open(PLAYERS_FILE, 'w', encoding='utf-8') as ini_file:
        players.write(ini_file)
    saves = ConfigParser()
    for pair in SAVES:
        player1, player2, turns = pair.keys()
        section = f"{player1};{player2}"
        saves[section] = {}
        saves[section]['turns'] = ','.join([str(i) for i in pair[turns]])
    with open('player_test.ini', 'w', encoding='utf-8') as ini_file:
        saves.write(ini_file)


if __name__ == '__main__':
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
