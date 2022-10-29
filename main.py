"""Модуль верхнего уровня: для учебного проекта Крестики-Нолики."""

# импорт из стандартной библиотеки
from importlib import reload

# импорт дополнительных модулей проекта
import data
import functions
import help
import gameset
import game


# 1. Чтение данных из текстовых файлов данных
# 2. ЕСЛИ первый запуск:
if functions.read_ini():
    # вывод раздела помощи
    help.show_help()
# 3. Запрос имени игрока
functions.get_player_name()
# print(data.STATS)


# суперцикл
while True:
    # 4. Ожидание ввода команды
    gameset.check_training()
    print(['', f"\nДоступны следующие команды:\n{help.show_command()}"][data.TRAINING])
    command = input(f"Введите команду{data.PROMPT}")

    # new
    if command in data.COMMANDS['начать новую партию']:
        FIRST_PLAYER = data.PLAYERS[0]
        # 5. Запрос режима игры:
        gameset.game_mode()
        gameset.check_training()
        # партия
        res = game.game()
        # 19. Удаление автосохранения и обновление статистики
        functions.update_stats(res)
        reload(data)
        functions.read_ini()
        data.PLAYERS = [FIRST_PLAYER]
    if command in data.COMMANDS['новый игрок']:
        reload(data)
        functions.read_ini()
        functions.get_player_name()
    if command in data.COMMANDS['восстановить игру']:
        FIRST_PLAYER = data.PLAYERS[0]
        functions.load()
        res = game.game(loaded=True)
        functions.update_stats(res)
        data.PLAYERS = [FIRST_PLAYER]
    if command in data.COMMANDS['включить режим обучения']:
        data.TRAINING = True
        help.show_help()
    elif command in data.COMMANDS['отобразить результаты']:
        functions.show_stats()
    elif command in data.COMMANDS['выйти из игры']:
        print(f"Ждем вас снова в игре {data.APP_TITLE}!")
        break

# 21. Обработка завершения работы приложения

# stdout:
# Введите имя игрока > Ioann
# Введите команду > new
# Введите режим игры: 1 - игра с ботом, 2 - игра с другим человеком > 2
# Введите имя игрока > Zhanna
# Введите каким знаком будете играть: X или O > O
# Введите номер ячейки для хода > 1
#
#   X |   |
#  ———————————
#     |   |
#  ———————————
#     |   |
#
# Введите номер ячейки для хода > 2
#
#                                                                    X | O |
#                                                                   ———————————
#                                                                      |   |
#                                                                   ———————————
#                                                                      |   |
#
# Введите номер ячейки для хода > 3
#
#   X | O | X
#  ———————————
#     |   |
#  ———————————
#     |   |
#
# Введите номер ячейки для хода > 4
#
#                                                                    X | O | X
#                                                                   ———————————
#                                                                    O |   |
#                                                                   ———————————
#                                                                      |   |
#
# Введите номер ячейки для хода > 5
#
#   X | O | X
#  ———————————
#   O | X |
#  ———————————
#     |   |
#
# Введите номер ячейки для хода > 6
#
#                                                                    X | O | X
#                                                                   ———————————
#                                                                    O | X | O
#                                                                   ———————————
#                                                                      |   |
#
# Введите номер ячейки для хода > 6
# Такой ход уже был, введите другой!
# Введите номер ячейки для хода > 12
# Вы ввели неверный номер ячейки для хода, введите от 1 до 9!
# Введите номер ячейки для хода > 7
#
#   X | O | X
#  ———————————
#   O | X | O
#  ———————————
#   X |   |
#
# Игрок Zhanna победил!
#
# Введите команду > new
# Введите режим игры: 1 - игра с ботом, 2 - игра с другим человеком > 1
# Введите уровень сложности игры с ботом: 1 - простой, 2 - сложный > 1
# Введите каким знаком будете играть: X или O > X
# Введите номер ячейки для хода > 1
#
#   X |   |
#  ———————————
#     |   |
#  ———————————
#     |   |
#
#
#                                                                    X |   |
#                                                                   ———————————
#                                                                    O |   |
#                                                                   ———————————
#                                                                      |   |
#
# Введите номер ячейки для хода > 3
#
#   X |   | X
#  ———————————
#   O |   |
#  ———————————
#     |   |
#
#
#                                                                    X |   | X
#                                                                   ———————————
#                                                                    O | O |
#                                                                   ———————————
#                                                                      |   |
#
# Введите номер ячейки для хода > 6
#
#   X |   | X
#  ———————————
#   O | O | X
#  ———————————
#     |   |
#
#
#                                                                    X |   | X
#                                                                   ———————————
#                                                                    O | O | X
#                                                                   ———————————
#                                                                    O |   |
#
# Введите номер ячейки для хода > 2
#
#   X | X | X
#  ———————————
#   O | O | X
#  ———————————
#   O |   |
#
# Игрок Ioann победил!
#
# Введите команду > table
# Игрок Ioann
# победил 12 раз, проиграл 7 раз, вничью 2 раз.
# Игрок Zhanna
# победил 4 раз, проиграл 7 раз, вничью 1 раз.
# Игрок #1
# победил 1 раз, проиграл 3 раз, вничью 0 раз.
# Игрок #2
# победил 1 раз, проиграл 0 раз, вничью 0 раз.
# Введите команду > quit
# Ждем вас снова в игре КРЕСТИКИ-НОЛИКИ!