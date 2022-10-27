"""Дополнительный модуль: вспомогательные функции."""

from configparser import ConfigParser
from shutil import get_terminal_size
import data
import functions

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


def get_player_name() -> None:
    """Запрашивает имя игрока и проверяет присутствие этого имени в глобальной переменной статистики, добавляет имя в глобальную переменную текущих игроков."""

    while True:
        player_name = input(f"Введите имя игрока{data.PROMPT}")
        if player_name == '':
            print('Имя игрока не может быть пустым!')
            continue
        if player_name.startswith('#'):
            print('Имя игрока не должно начинаться на "#"!')
            continue
        if player_name in data.PLAYERS:
            print('Игрок не может играть сам с собой!')
            continue
        else:
            if player_name not in data.STATS:
                data.STATS[player_name] = {'wins': 0, 'fails': 0, 'ties': 0, 'training': True}
                functions.write_ini()
                data.PLAYERS.append(player_name)
            else:
                data.PLAYERS.append(player_name)
            break

def draw_board(board: list[str], align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""
    max_width = len(max(board, key=lambda elem: len(elem)))
    centered_board = [elem.center(max_width + 2)
                      for elem in
                      [' ' * (max_width - len(i)) + i for i in board]]
    h_line = '—' * (data.DIM * (max_width + 2) + data.DIM - 1) + '\n'
    result = ''
    if align_right:
        align = get_terminal_size()[0] - 2
    else:
        align = len(h_line) + 1
    for i in data.RANGE:
        row = '|'.join(centered_board[i * data.DIM: (i + 1) * data.DIM])
        result += f"{row.rjust(align - 1)}\n"
    h_line = f"\n{h_line.rjust(align)}"
    result = result.rstrip('\n').replace('\n', h_line)
    return result


def update_stats(score: data.Score) -> None:
    """Обновляет глобальную переменную статистики в соответствии с результатом завершённой партии."""
    for elem in score:
        for player in elem:
            for results in elem.values():
                for result in results:
                    data.STATS[player][result] += results[result]
                    data.STATS[player]['training'] = False
    data.SAVES.pop(tuple(data.PLAYERS))
    functions.write_ini()


def show_stats() -> None:
    """Выводит в stdout статистику игроков."""
    for player in data.STATS:
        print(f"Игрок {player}\nпобедил {data.STATS[player]['wins']} раз, "
              f"проиграл {data.STATS[player]['fails']} раз, "
              f"вничью {data.STATS[player]['ties']} раз.")


if __name__ == '__main__':
    pass
    # functions.read_ini()
    # get_player_name()
    # read_ini()
    # print(draw_board(data.BOARD))
    # print(draw_board(data.BOARD, True))
    # get_player_name()
    # write_ini()

# stdout:
# BOARD = list(str(n) for n in range(1, 260, 10))
#     1 |  11 |  21 |  31 |  41
#  —————————————————————————————
#    51 |  61 |  71 |  81 |  91
#  —————————————————————————————
#   101 | 111 | 121 | 131 | 141
#  —————————————————————————————
#   151 | 161 | 171 | 181 | 191
#  —————————————————————————————
#   201 | 211 | 221 | 231 | 241
#                                                    1 |  11 |  21 |  31 |  41
#                                                 —————————————————————————————
#                                                   51 |  61 |  71 |  81 |  91
#                                                 —————————————————————————————
#                                                  101 | 111 | 121 | 131 | 141
#                                                 —————————————————————————————
#                                                  151 | 161 | 171 | 181 | 191
#                                                 —————————————————————————————
#                                                  201 | 211 | 221 | 231 | 241
