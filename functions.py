"""Дополнительный модуль: вспомогательные функции."""

from configparser import ConfigParser
from data import STATS, config_file


def load_ini(file: str, stats: dict) -> None:
    """Читает данные из ini-файла в глобальную переменную данных."""
    config = ConfigParser()
    config.read(file, encoding='utf-8')
    for section in config.sections():
        stats[section] = {
            key: int(value)
            for key, value in config[section].items()
        }


def write_ini(file: str, stats: dict) -> None:
    """Записывает данные из глобальной переменной данных в ini-файл."""
    config = ConfigParser()
    config.read_dict(stats)
    with open(file, 'w', encoding='utf-8') as ini_file:
        config.write(ini_file)


if __name__ == '__main__':
    load_ini(config_file, STATS)
    print(STATS)
    STATS['Player1']['wins'] = 3
    STATS['Player2']['fails'] = 1
    STATS['Ioann'] = {'wins': 0, 'fails': 0, 'ties': 0}
    write_ini(config_file, STATS)
    load_ini(config_file, STATS)
    print(STATS)
