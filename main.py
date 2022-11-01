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
    print(['', f"\nДоступны следующие команды:\n{help.show_commands()}"][data.TRAINING])
    command = input(f"Введите команду{data.PROMPT}")

    if command in data.COMMANDS['начать новую партию']:
        first_player = data.PLAYERS[0]
        # 5. Запрос режима игры:
        gameset.game_mode()
        gameset.check_training()
        # партия
        res = game.game()
        # 19. Удаление автосохранения и обновление статистики
        functions.update_stats(res)
        reload(data)
        functions.read_ini()
        data.PLAYERS = [first_player]

    if command in data.COMMANDS['новый игрок']:
        # ОТВЕТИТЬ: зачем перезагружать модуль перед добавлением нового игрока?
        reload(data)
        functions.read_ini()
        functions.get_player_name()
        # ДОБАВИТЬ: запись значения обновлённой глобальной переменной в файл

    if command in data.COMMANDS['восстановить игру']:
        first_player = data.PLAYERS[0]
        functions.load()
        res = game.game(loaded=True)
        functions.update_stats(res)
        data.PLAYERS = [first_player]

    if command in data.COMMANDS['включить режим обучения']:
        data.TRAINING = True
        help.show_help()

    if command in data.COMMANDS['отобразить результаты']:
        functions.show_stats()

    if command in data.COMMANDS['изменить размер поля']:
        functions.change_dimension(get_from_input=True)

    if command in data.COMMANDS['выйти из игры']:
        break

# 21. Обработка завершения работы приложения
print(f"Ждем вас снова в игре {data.APP_TITLE}!")
