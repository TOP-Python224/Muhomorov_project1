"""Дополнительный модуль: вспомогательные функции."""

from configparser import ConfigParser
from shutil import get_terminal_size
import data

players_file = './players.ini'
saves_file = './saves.ini'


def read_ini() -> bool:
    """Читает данные из ini-файлов в глобальные переменные данных."""
    players = ConfigParser()
    players.read(players_file, encoding='utf-8')
    for section in players.sections():
        data.STATS[section] = {
            key: int(value) if value.isdecimal() else value
            for key, value in players[section].items()
        }
    saves = ConfigParser()
    saves.read(saves_file, encoding='utf-8')
    for section in saves.sections():
        # ИСПОЛЬЗОВАТЬ: конвертацию в кортеж
        players = tuple(section.split(';'))
        turns = [int(i) for i in saves[section]['turns'].split(',')]
        data.SAVES[players] = turns
    if data.STATS:
        return False
    else:
        return True


def write_ini() -> None:
    """Записывает данные из глобальных переменных данных в ini-файлы."""
    players = ConfigParser()
    players.read_dict(data.STATS)
    with open(players_file, 'w', encoding='utf-8') as ini_file:
        players.write(ini_file)
    saves = ConfigParser()
    for save in data.SAVES:
        player1, player2 = list(save)
        section = f"{player1};{player2}"
        saves[section] = {}
        saves[section]['turns'] = ','.join([str(i) for i in data.SAVES[save]])
    with open(saves_file, 'w', encoding='utf-8') as ini_file:
        saves.write(ini_file)


def draw_board(align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""
    h_line = '—' * (data.DIM * 3 + data.DIM - 1) + '\n'
    result = ''
    if align_right:
        align = get_terminal_size()[0] - 1
    else:
        align = len(h_line) + 1
    for i in range(1, data.DIM + 1):
        result += f" {' | '.join(data.BOARD[i * data.DIM - data.DIM: i * data.DIM]).rjust(align - 3)} \n"
    h_line = f"\n{h_line.rjust(align)}"
    result = result.rstrip('\n').replace('\n', h_line)
    return result


if __name__ == '__main__':
    # print(draw_board())
    # print(draw_board(True))
    read_ini()
    write_ini()
    print(data.STATS)
    data.STATS['Player1']['wins'] = 3
    data.STATS['Player2']['fails'] = 1
    data.STATS['Ioann'] = {'wins': 0, 'fails': 0, 'ties': 0, 'training': 'True'}
    data.SAVES[('PlayerC', 'PlayerD')] = [1, 3, 6]
    write_ini()
    read_ini()
    print(data.STATS)
    print(data.SAVES)


# stdout:
#    |   |
# ———————————
#    |   |
# ———————————
#    |   |
#                                                                       |   |
#                                                                    ———————————
#                                                                       |   |
#                                                                    ———————————
#                                                                       |   |
#
# {'Player1': {'wins': 2, 'fails': 3, 'ties': 5, 'training': 'False'}, 'Player2': {'wins': 0, 'fails': 0, 'ties': 0, 'training': 'True'}}
# {'Player1': {'wins': 3, 'fails': 3, 'ties': 5, 'training': 'False'}, 'Player2': {'wins': 0, 'fails': 1, 'ties': 0, 'training': 'True'}, 'Ioann': {'wins': 0, 'fails': 0, 'ties': 0, 'training': 'False'}}
# {('PlayerA', 'PlayerB'): [3, 7, 4, 9, 5], ('#2', 'PlayerB'): [5, 7, 1], ('PlayerC', 'PlayerD'): [1, 3, 6]}
