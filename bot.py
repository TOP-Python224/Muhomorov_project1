"""Дополнительный модуль: искусственный интеллект."""

# импорт дополнительных модулей проекта
from random import choice

# импорт дополнительных модулей проекта
import data
import functions


def dumb_bot() -> int:
    """Возвращает случайный ход из доступного диапазона ходов."""
    return choice(list(set(data.ALL_TURNS) - set(data.TURNS))) - 1


def smart_bot() -> int:
    """Возвращает ход в соответствии с выигрышной стратегией."""
    bot_token_index = data.PLAYERS.index('#2')
    tw = weights_tokens(bot_token_index)
    ew = weights_empty(tw)
    if len(data.TURNS) < 2*data.DIM - 1:
        ew = matrix_add(ew, data.BOT_SM[bot_token_index])
    weights_clear(tw, ew)
    if any(vectorization(ew)):
        return index_of_rand_max(vectorization(ew))
    else:
        return dumb_bot()


def weights_tokens(token_index: int) -> data.Matrix:
    """Конструирует и возвращает матрицу весов занятых ячеек игрового поля."""
    board = matricization(data.BOARD)
    tokensweights = [[0]*data.DIM for _ in data.RANGE]
    for i in data.RANGE:
        for j in data.RANGE:
            try:
                if board[i][j] == data.TOKENS[token_index]:
                    tokensweights[i][j] = data.WEIGHT_OWN
                elif board[i][j] == data.TOKENS[token_index-1]:
                    tokensweights[i][j] = data.WEIGHT_FOE
            except IndexError:
                pass
    return tokensweights


def weights_empty(tokensweights: data.Matrix) -> data.Matrix:
    """Вычисляет и возвращает матрицу весов пустых ячеек игрового поля."""
    emptyweights = [[0]*data.DIM for _ in data.RANGE]
    weights = {data.WEIGHT_OWN, data.WEIGHT_FOE}
    for i in data.RANGE:
        for j in data.RANGE:
            if not tokensweights[i][j]:
                series = [
                    get_row(tokensweights, i),
                    get_column(tokensweights, j),
                    get_maindiag(tokensweights, i, j),
                    get_antidiag(tokensweights, i, j)
                ]
                for seq in series:
                    if not (weights <= set(seq)):
                        emptyweights[i][j] += sum(seq)**2
                emptyweights[i][j] = int(emptyweights[i][j])
    return emptyweights


def weights_clear(tokensweights: data.Matrix,
                  solvingweights: data.Matrix) -> None:
    """Обрабатывает матрицу принятия решения, приравнивая к нолю элементы, соответствующие занятым на поле клеткам."""
    for i in data.RANGE:
        for j in data.RANGE:
            if tokensweights[i][j]:
                solvingweights[i][j] = 0


def vectorization(matrix: data.Matrix) -> data.Series:
    """Возвращает плоскую последовательность, полученную в результате преобразования переданной матрицы."""
    return [cell for row in matrix for cell in row]


def matricization(sequence: data.Series) -> data.Matrix:
    """Возвращает квадратную матрицу, полученную в результате преобразования переданной плоской последовательности."""
    return [sequence[i*data.DIM:(i+1)*data.DIM] for i in data.RANGE]


def get_row(matrix: data.Matrix,
            row_index: int) -> data.Series:
    """Возвращает ряд матрицы по переданному индексу."""
    return matrix[row_index]


def get_column(matrix: data.Matrix,
               column_index: int) -> data.Series:
    """Возвращает столбец матрицы по переданному индексу."""
    return [row[column_index] for row in matrix]


def get_maindiag(matrix: data.Matrix,
                 row_index: int,
                 column_index: int) -> data.Series:
    """Возвращает главную диагональ матрицы, если элемент по переданным индексам ей принадлежит."""
    if row_index == column_index:
        return [matrix[i][i] for i in data.RANGE]
    return []


def get_antidiag(matrix: data.Matrix,
                 row_index: int,
                 column_index: int) -> data.Series:
    """Возвращает побочную диагональ матрицы, если элемент по переданным индексам ей принадлежит."""
    if row_index == data.DIM - column_index - 1:
        return [matrix[i][-i-1] for i in data.RANGE]
    return []


def matrix_add(matrix1: data.Matrix,
               matrix2: data.Matrix,
               *matrices: data.Matrix) -> data.Matrix:
    """Возвращает результат математического сложения двух и более матриц."""
    matrices = (matrix1, matrix2) + matrices
    result = [[0]*data.DIM for _ in data.RANGE]
    for i in data.RANGE:
        for j in data.RANGE:
            result[i][j] = sum(m[i][j] for m in matrices)
    return result


def index_of_rand_max(series: data.Series) -> int:
    """Возвращает индекс случайного среди равных максимальных значений в последовательности."""
    m = max(series)
    return choice([i for i, v in enumerate(series) if v == m])


# переменные модуля
data.BOT_SM = (
    functions.calc_sm_cross(),
    functions.calc_sm_zero()
)


if __name__ == '__main__':
    functions.change_dimension(7)
    smc = functions.calc_sm_cross()
    smz = functions.calc_sm_zero()
    print(functions.draw_board(vectorization(smc)), end='\n\n')
    print(functions.draw_board(vectorization(smz)), end='\n\n')
