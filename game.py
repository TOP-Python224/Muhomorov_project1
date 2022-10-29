"""Дополнительный модуль: партия."""

# импорт дополнительных модулей проекта
import data
import functions
import bot


def human_turn() -> int:
    """Запрашивает у игрока и возвращает корректную координату ячейки поля для текущего хода, после 1-го хода производит автосохранение результатов."""
    while True:
        curr_turn = input(f"Введите номер ячейки для хода{data.PROMPT}")
        if curr_turn == '':
            if len(data.PLAYERS) == 2 and len(data.TURNS) > 0:
                data.SAVES[tuple(data.PLAYERS)] = data.TURNS
                functions.write_ini()
            continue
        if curr_turn.isdecimal():
            curr_turn = int(curr_turn)
        else:
            print(f"Вы ввели неверный номер ячейки для хода, введите от 1 до {data.DIM**2}!")
            continue
        if curr_turn < 1 or curr_turn > data.DIM**2:
            print(f"Вы ввели неверный номер ячейки для хода, введите от 1 до {data.DIM**2}!")
            continue
        if data.BOARD[curr_turn-1] != '':
            print(f"Такой ход уже был, введите другой!")
            continue
        else:
            remove_reverse = tuple(list(reversed(data.PLAYERS)))
            # print(data.SAVES)
            # print(remove_reverse)
            if remove_reverse in data.SAVES:
                data.SAVES.pop(remove_reverse)
                # print(data.SAVES)
                # print('OK!!!!!')
            return curr_turn - 1


def bot_turn() -> int:
    """Вычисляет и возвращает координату ячейки поля для текущего хода бота в зависимости от сложности."""
    return [bot.dumb_bot, bot.smart_bot][data.BOT_LEVEL-1]()


def check_win() -> bool:
    """Проверяет текущую партию на наличие победной комбинации."""
    win = False

    def check_line(line: list[str]):
        """Проверяет наличие выигрышной комбинации в каждой строке, каждом столбце и каждой диагонали."""
        nonlocal win
        if all(line) and len(set(line)) == 1:
            win = True

    for i in data.RANGE:
        row = data.BOARD[i*data.DIM: (i+1) * data.DIM]
        check_line(row)
        column = data.BOARD[i::data.DIM]
        check_line(column)
    diagonals = data.BOARD[::data.DIM+1], data.BOARD[data.DIM-1: -1: data.DIM-1]
    for diagonal in diagonals:
        check_line(diagonal)
    return win


def game(loaded: bool = False) -> data.Score | None:
    """Управляет игровым процессом для каждой новой или загруженной партии."""
    if loaded:
        turns_cnt = len(data.TURNS)
        token_index = turns_cnt % 2
    else:
        turns_cnt = 1
        token_index = 0
    turns = [human_turn, human_turn]
    for player in data.PLAYERS:
        if player.startswith('#'):
            turns[data.PLAYERS.index(player)] = bot_turn
    while True:
        print(['', f"Ход игрока '{data.PLAYERS[token_index]}'"][data.TRAINING])
        curr_turn = turns[token_index]()
        data.BOARD[curr_turn] = data.TOKENS[token_index]
        data.TURNS.append(curr_turn+1)
        data.SAVES[tuple(data.PLAYERS)] = data.TURNS
        functions.write_ini()
        print(f"\n{functions.draw_board(data.BOARD, token_index)}\n")
        print(f"{['', functions.print_tutorial(curr_turn, token_index, token_index)][data.TRAINING]}")
        if check_win():
            print(f"Игрок '{data.PLAYERS[token_index]}' победил!\n")
            return {data.PLAYERS[token_index]: {'wins': 1, 'training': False}}, \
                   {data.PLAYERS[abs(token_index-1)]: {'fails': 1, 'training': False}}
        token_index = abs(token_index-1)
        turns_cnt += 1
        if turns_cnt > data.DIM**2 and not check_win():
            print(f"Ничья!\n")
            return {data.PLAYERS[0]: {'ties': 1, 'training': False}}, \
                   {data.PLAYERS[1]: {'ties': 1, 'training': False}}


# тесты
if __name__ == '__main__':
    print(functions.draw_board(data.BOARD))
    print(check_win())
    print(human_turn())
