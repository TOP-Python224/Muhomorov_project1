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
            # ОТВЕТИТЬ: первое условие избыточно, считаю
            # Ловил глюк, связанный с этим, был только 1 игрок в списке, воссоздать не удалось, удаляю.
            if len(data.TURNS) > 0:
            # if len(data.PLAYERS) == 2 and len(data.TURNS) > 0:
                data.SAVES[tuple(data.PLAYERS)] = [data.TURNS, data.DIM]
                functions.write_ini()
            # ИСПРАВИТЬ: надо бы выйти из игры, зачем запрашивать всё новый и новый ход — это же должно быть досрочное завершение партии
            # Я понял ТЗ так, что при вводе пустого хода должно производиться автосохранение. От себя добавил проверку, что хотя бы 1 ход был, чтобы не сохранять пустые данные. Опять же игрок может по ошибке нажать Enter, или случайно дваджы нажать после своего хода, если после этого сразу завершать игру, то какой-то недружественный интерфейс получается.
            continue
        if curr_turn.isdecimal():
            curr_turn = int(curr_turn)
        else:
            print(f"Вы ввели неверный номер ячейки для хода, введите от 1 до {data.CELLS}!")
            continue
        if curr_turn < 1 or curr_turn > data.CELLS:
            print(f"Вы ввели неверный номер ячейки для хода, введите от 1 до {data.CELLS}!")
            continue
        if data.BOARD[curr_turn-1] != '':
            print(f"Такой ход уже был, введите другой!")
            continue
        else:
            return curr_turn - 1


def bot_turn() -> int:
    """Вычисляет и возвращает координату ячейки поля для текущего хода бота в зависимости от сложности."""
    return [bot.dumb_bot, bot.smart_bot][data.BOT_LEVEL-1]()


def check_win() -> bool:
    """Проверяет текущую партию на наличие победной комбинации."""
    all_lines = []
    for i in data.RANGE:
        all_lines += [data.BOARD[i*data.DIM:(i+1)*data.DIM]]
        all_lines += [data.BOARD[i::data.DIM]]
    diagonals = data.BOARD[::data.DIM+1], data.BOARD[data.DIM-1:-1:data.DIM-1]
    all_lines += diagonals
    for line in all_lines:
        if all(line) and len(set(line)) == 1:
            return True
    return False


def game(loaded: bool = False) -> data.Score | None:
    """Управляет игровым процессом для каждой новой или загруженной партии."""
    remove_reverse = tuple(reversed(data.PLAYERS))
    data.PLAYERS = tuple(data.PLAYERS)
    if loaded:
        turns_cnt = len(data.TURNS)
        token_index = turns_cnt % 2
    else:
        turns_cnt = 1
        token_index = 0
    # КОММЕНТАРИЙ: тоже хорошее решение, одобряю
    turns = [human_turn, human_turn]
    for player in data.PLAYERS:
        if player.startswith('#'):
            turns[data.PLAYERS.index(player)] = bot_turn
    while True:
        print(['', f"Ход игрока '{data.PLAYERS[token_index]}'"][data.TRAINING])
        curr_turn = turns[token_index]()
        data.BOARD[curr_turn] = data.TOKENS[token_index]
        data.TURNS.append(curr_turn+1)
        # ИСПРАВИТЬ: полагаю, коли так, то лучше ещё на инициализации сделать data.PLAYERS кортежем, а не списком, и не выполнять лишнее преобразование на каждой итерации
        data.SAVES[data.PLAYERS] = [data.TURNS, data.DIM]
        if len(data.TURNS) == 1 and remove_reverse in data.SAVES:
            data.SAVES.pop(remove_reverse)
        functions.write_ini()
        print(f"\n{functions.draw_board(data.BOARD, token_index)}\n")
        print(f"{['', functions.print_tutorial(curr_turn, token_index, token_index)][data.TRAINING]}")
        if check_win():
            print(f"Игрок '{data.PLAYERS[token_index]}' победил!\n")
            return {data.PLAYERS[token_index]: {'wins': 1, 'training': False}}, \
                   {data.PLAYERS[abs(token_index-1)]: {'fails': 1, 'training': False}}
        token_index = abs(token_index-1)
        turns_cnt += 1
        if turns_cnt > data.CELLS and not check_win():
            print(f"Ничья!\n")
            return {data.PLAYERS[0]: {'ties': 1, 'training': False}}, \
                   {data.PLAYERS[1]: {'ties': 1, 'training': False}}
