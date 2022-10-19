from shutil import get_terminal_size as gts
from data import *

width_screen = gts()[0]
board = list(' ' * 9)
# board = ['X', '0', 'X',
#              'X', '0', 'X',
#              '0 ', 'X', '0']
# h_line = f"{11 * '—'}"
# move = input('Введите номер клетки от 1 до 9 для хода: ')
#
# board[int(inp)] = 'X'

"""
 1 | 2 | 3
——————————
 4 | 5 | 6 
———————————
 7 | 8 | 9 
"""


# str0 = f" {board[0]} | {board[1]} | {board[2]} "
# str1 = f" {board[3]} | {board[4]} | {board[5]} "
# str2 = f" {board[6]} | {board[7]} | {board[8]} "
# str0 = f" {{board[0]} | {board[1]} | {board[2]}.rjust(width_screen)} "
# print(str0)
# print(h_line)
# print(str1)
# print(h_line)
# print(str2)

# print(str0.rjust(width_screen - 1))
# print(h_line.rjust(width_screen - 1))
# print(str1.rjust(width_screen - 1))
# print(h_line.rjust(width_screen - 1))
# print(str2.rjust(width_screen - 1))


# print(str0.rjust(width_screen))
# str1 = f" {11 * '—'}"
# print(str1.rjust(width_screen))
#  {board[3]} | {board[4]} | {board[5]} \n\
# {11 * '—'} \n\
#  {board[6]} | {board[7]} | {board[8]}")

# if all([board[0], board[4], board[8]]):
#     print('Ok!')

def check_board() -> bool:
    """Проверяет наличие выигрышной комбинации для текущей игровой ситуации."""
    for i in (0, 3, 6):
        if board[i] == board[i + 1] == board[i + 2]:
            return True
    for i in (0, 1, 2):
        if board[i] == board[i + 3] == board[i + 6]:
            return True
    if board[0] == board[4] == board[8]\
       or board[2] == board[4] == board[6]:
        return True


# print(check_board())

def check_curr_move() -> str:
    """Запрашивает номер клетки для хода, проверяет его на корректность и на уникальность."""
    game_chars = ['0', 'X']
    turns_cnt = 0
    while True:
        if turns_cnt >= 9:
            break
        curr_move = int(input('Введите номер клетки от 1 до 9 для хода: '))
        if curr_move < 1 or curr_move > 9:
            print('Вы ввели неверный номер клетки для хода, введите от 1 до 9: ')
        if board[curr_move - 1] != ' ':
            print('Вы уже вводили такой номер клетки, введите другой: ')
        else:
            board[curr_move - 1] = game_chars[0]
            game_chars.reverse()
            turns_cnt += 1

    # print(curr_move)


check_curr_move()
print(board)
