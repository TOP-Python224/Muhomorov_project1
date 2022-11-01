"""Дополнительный модуль: справка и обучение."""

# импорт дополнительных модулей проекта
import data
import functions


def show_help() -> None:
    """Выводит в stdout раздел помощи."""
    result = ''
    print(f"\n{data.APP_TITLE}\n")
    with open('./help.txt', encoding='utf-8') as help_text:
        for line in help_text:
            result += line
    result = result.replace('###', show_commands())
    print(f"{result}")
    print(f"{functions.draw_board(data.ALL_TURNS)}\n")
    print(f"Желаем удачи в игре {data.APP_TITLE}!")


def show_commands() -> str:
    """Выдает список доступных команд."""
    result = ''
    for k, v in data.COMMANDS.items():
        result += f"{list(v)} - {k},\n"
    result = result.rstrip(',\n')
    result += '.'
    return result


if __name__ == '__main__':
    show_help()
