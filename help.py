"""Дополнительный модуль: справка и обучение."""
import data
import functions


def show_help() -> None:
    """Выводит в stdout раздел помощи."""
    print(f"\n{data.APP_TITLE}\n")
    with open('./help.txt', encoding='utf-8') as help_text:
        for line in help_text:
            print(line, end='')
    print(f"\n{functions.draw_board([str(i) for i in range(1, data.DIM ** 2 + 1)])}\n")
    print(f"Желаем удачи в игре {data.APP_TITLE}!")


# show_help()

