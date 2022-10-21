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


# ДОБАВИТЬ: а теперь самое время добавить параметр, в который передавать нужную матрицу — ведь мы можем использовать эту функцию не только с глобальной переменной board (см. комментарий к тесту ниже)
def draw_board(align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""
    # КОММЕНТАРИЙ: ширина клетки не обязательно составляет ровно три символа — строго говоря она вообще может быть примерно любой (см. тесты ниже)
    h_line = '—' * (data.DIM*3 + data.DIM - 1) + '\n'
    result = ''
    if align_right:
        align = get_terminal_size()[0] - 1
    else:
        align = len(h_line) + 1
    for i in data.RANGE:
        # СДЕЛАТЬ: можно позже, но я бы сделал всё-таки отдельно центрирование каждой клетки по вычисленной ширине — тогда и вот эти неочевидные пробелы в разделителе и в начале/конце ряда не понадобятся
        row = ' | '.join(data.BOARD[i*data.DIM:(i+1)*data.DIM])
        result += f" {row.rjust(align-3)} \n"
    h_line = f"\n{h_line.rjust(align)}"
    # КОММЕНТАРИЙ: а вот это изящно, хвалю
    result = result.rstrip('\n').replace('\n', h_line)
    return result


if __name__ == '__main__':
    print(draw_board())
    print(draw_board(True))


# stdout:
# для DIM = 3, BOARD = [' '] * DIM**2
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

# для DIM = 3, BOARD = ['X', 'X', '0', '0', 'X', 'X', '0', '0', 'X']
#  X | X | 0
# ———————————
#  0 | X | X
# ———————————
#  0 | 0 | X
#                                                                    X | X | 0
#                                                                   ———————————
#                                                                    0 | X | X
#                                                                   ———————————
#                                                                    0 | 0 | X

# КОММЕНТАРИЙ: когда вы захотите использовать эту же функцию на большом поле для вывода подсказки игроку, какой выводить номер клетки, то столкнётесь с таким поведением — а всё из-за того, что у вас подразумевается ширина клетки всегда три символа, и ширина горизонтального разделителя рассчитывается из этой статичной ширин — как видите, это не всегда так
# для DIM = 5, BOARD = list(str(n) for n in range(1, 26))
#   1 | 2 | 3 | 4 | 5
#  ———————————————————
#  6 | 7 | 8 | 9 | 10
#  ———————————————————
#  11 | 12 | 13 | 14 | 15
#  ———————————————————
#  16 | 17 | 18 | 19 | 20
#  ———————————————————
#  21 | 22 | 23 | 24 | 25
#                                                             1 | 2 | 3 | 4 | 5
#                                                            ———————————————————
#                                                            6 | 7 | 8 | 9 | 10
#                                                            ———————————————————
#                                                        11 | 12 | 13 | 14 | 15
#                                                            ———————————————————
#                                                        16 | 17 | 18 | 19 | 20
#                                                            ———————————————————
#                                                        21 | 22 | 23 | 24 | 25

# КОММЕНТАРИЙ: на будущее: помимо большого поля, может понадобиться выводить и другие объекты, например, весовые матрицы для отладки бота
# для DIM = 3, BOARD = list(map(str, [0, 1.5, 1, 0, 0, 1, 1.5, 1.5, 1]))
#  0 | 1.5 | 1
#  ———————————
#   0 | 0 | 1
#  ———————————
#  1.5 | 1.5 | 1
#                                                                   0 | 1.5 | 1
#                                                                    ———————————
#                                                                     0 | 0 | 1
#                                                                    ———————————
#                                                                 1.5 | 1.5 | 1
