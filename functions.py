"""Дополнительный модуль: вспомогательные функции."""

# ИСПОЛЬЗОВАТЬ: имя ConfigParser на практике не используется в длинных выражениях, так что один–два раза можно его написать и целиком — зато не придётся гадать, что за cp
from configparser import ConfigParser
from data import STATS, config_file


def load_ini(file: str, stats: dict) -> None:
    """Читает данные из ini-файла в глобальную переменную данных."""
    config = ConfigParser()
    config.read(file, encoding='utf-8')
    for section in config.sections():
        stats[section] = {
            key: int(value)
            # ИСПОЛЬЗОВАТЬ: объект config и его элементы являются словароподобными и могут использовать в частности метод items()
            for key, value in config[section].items()
        }


def write_ini(file: str, stats: dict) -> None:
    """Записывает данные из глобальной переменной данных в ini-файл."""
    config = ConfigParser()
    # КОММЕНТАРИЙ: вот это хорошо, молодец
    config.read_dict(stats)
    with open(file, 'w', encoding='utf-8') as ini_file:
        # ИСПРАВИТЬ: а вот здесь ошибка: метод write() принимает на вход только файлоподобный объект и логический ключ — данные для записи считываются из объекта config, от которого вызывается метод
        config.write(ini_file)


# ИСПОЛЬЗОВАТЬ: в дополнительных модулях проекта тесты убираем под проверку импорта, чтобы лишний код не выполнялся/выводился во время импорта из других модулей
if __name__ == '__main__':
    load_ini(config_file, STATS)
    print(STATS)
    STATS['Player1']['wins'] = 3
    STATS['Player2']['fails'] = 1
    STATS['Ioann'] = {'wins': 0, 'fails': 0, 'ties': 0}
    write_ini(config_file, STATS)
    load_ini(config_file, STATS)
    print(STATS)


# std_out:
# {'Player1': {'wins': '2', 'fails': '3', 'ties': '5'}, 'Player2': {'wins': '0', 'fails': '0', 'ties': '0'}}
# {'Player1': {'wins': '3', 'fails': '3', 'ties': '5'}, 'Player2': {'wins': '0', 'fails': '1', 'ties': '0'}, 'Ioann': {'wins': '0', 'fails': '0', 'ties': '0'}}