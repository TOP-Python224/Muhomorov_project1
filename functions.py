"""Дополнительный модуль: вспомогательные функции."""
from configparser import ConfigParser as cp
from data import STATS, config_file


def load_ini(file: str, stats: dict) -> None:
    """Читает данные из ini-файла в словарь."""
    config = cp()
    config.read(file, encoding='utf-8')
    for section in config.sections():
        stats[section] = {key: int(config[section][key]) for key in config[section]}


def write_ini(file: str, stats: dict) -> None:
    """Записывает данные из словаря в ini-файл."""
    config = cp()
    config.read_dict(stats)
    with open(file, 'w', encoding='utf-8') as ini_file:
        config.write(ini_file, stats)


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