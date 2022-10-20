"""Дополнительный модуль: искусственный интеллект."""

from random import choice
import data

all_turns = {i for i in range(1, 10)}


def dump_bot() -> int:
    """Возвращает случайный ход из доступного диапазона ходов."""
    return choice(list(all_turns - set(data.TURNS)))


if __name__ == '__main__':
    print(dump_bot())
