"""Дополнительный модуль: настройка партии."""

# импорт дополнительных модулей проекта
import data
import functions


def game_mode() -> None:
    """Запрашивает режим для новой партии, при необходимости выполняет запросы уровня сложности или имени второго игрока, выполняет запрос очерёдности ходов."""
    while True:
        mode = input(f"Введите режим игры: 1 - игра с ботом, 2 - игра с другим человеком{data.PROMPT}")
        if mode not in ('1', '2'):
            print('Вы ввели некорректный режим игры!')
            continue
        else:
            if mode == '1':
                get_bot_level()
            else:
                functions.get_player_name()
        get_turn_order()
        break


def get_bot_level() -> None:
    """Запрашивает уровень сложности для режима игры с ботом, добавляет имя бота в глобальную переменную текущих игроков."""
    while True:
        level = input(f"Введите уровень сложности игры с ботом: 1 - простой, 2 - сложный{data.PROMPT}")
        if level not in ('1', '2'):
            print('Вы ввели некорректный уровень сложности игры!')
            continue
        else:
            data.BOT_LEVEL = int(level)
            level = '#' + level
            data.PLAYERS.append(level)
            if level not in data.STATS:
                data.STATS[level] = {'wins': 0, 'fails': 0, 'ties': 0, 'training': 'False'}
            functions.write_ini()
            break


def get_turn_order() -> None:
    """Запрашивает текущего активного игрока о его выборе токена для партии, при необходимости меняет порядок имён в глобальной переменной текущих игроков."""
    while True:
        token = input(f"Введите каким знаком будете играть: {' или '.join(data.TOKENS)}{data.PROMPT}")
        if token.upper() not in data.TOKENS:
            print('Вы ввели некорректный знак!')
            continue
        else:
            # ИСПРАВИТЬ:
            # Если активный игрок выбрал 'O', то он меняется местами с другим игроком в data.PLAYERS.
            if token.upper() == 'O':
                data.PLAYERS.reverse()
        print()
        break


def check_training() -> None:
    """Проверяет, является ли данная партия первой для любого из игроков и устанавливает глобальную переменную. """
    for player in data.PLAYERS:
        if data.STATS[player]['training'] == 'True':
            data.TRAINING = True
