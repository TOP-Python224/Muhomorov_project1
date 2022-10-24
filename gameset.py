"""Дополнительный модуль: настройка партии."""
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
            if level == '1':
                data.PLAYERS.append('#1')
                if '#1' not in data.STATS:
                    data.STATS['#1'] = {'wins': 0, 'fails': 0, 'ties': 0, 'training': False}
                    functions.write_ini()
            else:
                data.PLAYERS.append('#2')
                if '#2' not in data.STATS:
                    data.STATS['#2'] = {'wins': 0, 'fails': 0, 'ties': 0, 'training': False}
                    functions.write_ini()
            break


def get_turn_order() -> None:
    """Запрашивает текущего активного игрока о его выборе токена для партии, при необходимости меняет порядок имён в глобальной переменной текущих игроков."""
    while True:
        token = input(f"Введите каким знаком будете играть: X или O{data.PROMPT}")
        if token not in data.TOKENS:
            print('Вы ввели некорректный знак!')
            continue
        else:
            if token == 'O':
                data.PLAYERS.reverse()
        break



def check_training() -> bool:
    """Проверяет, является ли данная партия первой для любого из игроков."""
    training = False
    for player in data.PLAYERS:
        if data.STATS[player]['training'] == 'True':
            training = True
    return training


# game_mode()
# functions.read_ini()
# print(check_training())
