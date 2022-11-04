"""Дополнительный модуль: вспомогательные функции."""

# импорт из стандартной библиотеки
from configparser import ConfigParser
from shutil import get_terminal_size

# импорт дополнительных модулей проекта
import data
import help

# переменные модуля
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
        players = tuple(section.split(';'))
        turns = [int(t) for t in saves[section]['turns'].split(',')]
        dimension = int(saves[section]['dimension'])
        data.SAVES[players] = [turns, dimension]
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
    # ИСПОЛЬЗОВАТЬ: кажется, так всё-таки удобнее и читабельнее
    for players, game_data in data.SAVES.items():
        section = ';'.join(players)
        turns = ','.join([str(t) for t in game_data[0]])
        dimension = str(game_data[1])
        saves[section] = {'turns': turns, 'dimension': dimension}
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
            # КОММЕНТАРИЙ: так-то может )) но вот статистику при этом вести — та ещё головная боль, здесь согласен =)
            print('Игрок не может играть сам с собой!')
            continue
        else:
            if player_name not in data.STATS:
                data.STATS[player_name] = {'wins': 0, 'fails': 0, 'ties': 0, 'training': 'True'}
                # Перенёс в main
                # write_ini()
                help.show_help()
            # ИСПОЛЬЗОВАТЬ: это действие происходит в любом случае, так что выносим его за пределы условной конструкции и не дублируем код
            data.PLAYERS.append(player_name)
            break


def draw_board(board: data.Series, align_right: bool = False) -> str:
    """Формирует и возвращает строку, содержащую псевдографическое изображение игрового поля со сделанными ходами."""
    board = [str(c) for c in board]
    max_width = len(max(board, key=lambda elem: len(elem)))
    # ИСПОЛЬЗОВАТЬ: здесь было лишнее преобразование вложенным циклом, результатом которого было не центрирование а выравнивание вправо в ячейке + один пробел, хотя того же эффекта можно достичь и без дополнительных циклов
    centered_board = [
        elem.rjust(max_width + 1)
        for elem in board
    ]
    h_line = '—'*(data.DIM*(max_width+2) + data.DIM - 1) + '\n'
    result = ''
    if align_right:
        align = get_terminal_size()[0] - 2
    else:
        align = len(h_line) + 1
    for i in data.RANGE:
        row = ' |'.join(centered_board[i*data.DIM:(i+1)*data.DIM])
        result += f"{row.rjust(align - 2)}\n"
    h_line = f"\n{h_line.rjust(align)}"
    # КОММЕНТАРИЙ: изящное решение
    result = result.rstrip('\n').replace('\n', h_line)
    return result


def print_tutorial(curr_turn: int, token_index: int, align_right: bool = False) -> str:
    """Формирует и возвращает строку, с подсказкой о текущем ходе, необходимой для режима обучения."""
    result = f"Игрок '{data.PLAYERS[token_index]}' сделал ход '{data.TOKENS[token_index]}' на ячейку '{curr_turn+1}'"
    if align_right:
        align = get_terminal_size()[0] - 3
    else:
        align = len(result)
    return result.rjust(align)


def update_stats(score: data.Score) -> None:
    """Обновляет глобальную переменную статистики в соответствии с результатом завершённой партии."""
    for elem in score:
        for player in elem:
            for results in elem.values():
                for result in results:
                    data.STATS[player][result] += results[result]
                    data.STATS[player]['training'] = False
    data.SAVES.pop(tuple(data.PLAYERS))
    write_ini()


def show_stats() -> None:
    """Выводит в stdout статистику игроков."""
    for player in data.STATS:
        print(f"Игрок {player}\nпобедил {data.STATS[player]['wins']} раз, "
              f"проиграл {data.STATS[player]['fails']} раз, "
              f"вничью {data.STATS[player]['ties']} раз.")


def load() -> None:
    """Загружает выбранную сохраненную партию."""
    saves_slots = load_slots()
    slot = get_slot(saves_slots)
    load_saves(slot, saves_slots)


def load_slots() -> dict:
    """Возвращает словарь с доступными сохраненными партиями для текущего игрока."""
    saves_slots = {}
    cnt = 1
    if data.SAVES:
        for players, save in data.SAVES.items():
            if data.PLAYERS[0] in players:
                saves_slots[cnt] = players, save
                cnt += 1
        return saves_slots


def get_slot(saves_slots: dict) -> int:
    """Запрашивает и возвращает номер сохраненной партии из выведенного списка."""
    if saves_slots:
        print(f"\nДоступны следующие сохраненные партии:")
        for k, v in saves_slots.items():
            print(k, v[0], sep=' = ')
    else:
        print('Нет доступных сохранений!')
    while True:
        slot = input(f"\nВведите номер сохраненной партии{data.PROMPT}")
        if slot.isdecimal():
            slot = int(slot)
            if slot in saves_slots:
                return slot
            else:
                print('Вы ввели некорректный номер сохраненной партии!')
        else:
            print('Вы ввели некорректный номер сохраненной партии')


def load_saves(slot: int, saves_slots: dict) -> None:
    """Загружает данные выбранной партии в глобальные переменные, выводит 2 последних хода."""
    data.PLAYERS = [*saves_slots[slot][0]]
    data.TURNS = saves_slots[slot][1][0]
    saves_dim = saves_slots[slot][1][1]
    if saves_dim > data.DIM:
        change_dimension(saves_dim)
    token_index = 0
    if len(data.TURNS) < 2:
        print('Сохраненные ходы не отображаются, т.к. сохранено менее 2-х ходов!')
        need_draw = []
    else:
        need_draw = data.TURNS[-2:]
    for turn in data.TURNS:
        print(data.BOARD)
        data.BOARD[turn-1] = data.TOKENS[token_index]
        if turn in need_draw:
            print(f"{print_tutorial(turn-1, token_index, token_index)}\n")
            print(f"{draw_board(data.BOARD, token_index)}\n")
        token_index = abs(token_index-1)


def calc_sm_cross() -> data.Matrix:
    """Вычисляет и возвращает начальную матрицу стратегии крестика."""
    sm_cross = [[0]*data.DIM for _ in data.RANGE]
    half, rem = divmod(data.DIM, 2)
    diag = list(range(1, half+1)) + list(range(half+rem, 0, -1))
    for i in data.RANGE:
        sm_cross[i][i] = diag[i]
        sm_cross[i][-i-1] = diag[i]
    return sm_cross


def calc_sm_zero() -> data.Matrix:
    """Вычисляет и возвращает начальную матрицу стратегии нолика."""

    def triangle_desc(n: int, start: int) -> data.Matrix:
        """Генерирует и возвращает верхне-треугольную по побочной диагонали матрицу, заполняемую параллельно побочной диагонали значениями по убыванию."""
        flat = []
        indexes = range(n)
        for i in indexes:
            flat += [m if m > 0 else 0 for m in range(start-i, -start, -1)][:n]
        matrix = [flat[i*n:(i+1)*n] for i in indexes]
        if n > 2:
            for i in indexes:
                for j in indexes:
                    if i > n-j-1:
                        matrix[i][j] = 0
        return matrix

    def rot90(matrix: data.Matrix) -> data.Matrix:
        """Возвращает "повёрнутую" на 90° матрицу."""
        indexes = range(len(matrix))
        matrix = [[matrix[j][i] for j in indexes] for i in indexes]
        for i in indexes:
            matrix[i] = matrix[i][::-1]
        return matrix

    half, rem = divmod(data.DIM, 2)
    quarter = triangle_desc(half, half+rem)
    if data.DIM > 6:
        for i in range(half):
            for j in range(half):
                if i == half-j-1:
                    if i != j:
                        quarter[i][j] -= 1
                if i > half-j:
                    quarter[i][i] = half - i - (rem+1)%2
    m1 = quarter
    m2 = rot90(m1)
    m3 = rot90(m2)
    m4 = rot90(m3)
    top, bot = [], []
    for i in range(half):
        top += [m1[i] + [0]*rem + m2[i]]
        bot += [m4[i] + [0]*rem + m3[i]]
    return top + [[0]*data.DIM]*rem + bot


def change_dimension(new_dimension: int = 3, get_from_input: bool = False) -> None:
    """Пересчитывает значения глобальных переменных при изменении размерности игрового поля."""
    if get_from_input:
        while True:
            new_dimension = input(f'Введите новый размер поля{data.PROMPT}')
            if not new_dimension.isdecimal() or int(new_dimension) not in range(3, 31):
                print('Введите целое число от 3 до 30')
                continue
            new_dimension = int(new_dimension)
            break
    data.DIM = new_dimension
    data.CELLS = new_dimension**2
    data.RANGE = range(new_dimension)
    data.ALL_TURNS = range(1, data.CELLS+1)
    data.BOARD = ['']*data.CELLS
    data.BOT_SM = (
        calc_sm_cross(),
        calc_sm_zero()
    )


if __name__ == '__main__':
    change_dimension(5)
    print(draw_board(data.ALL_TURNS))
