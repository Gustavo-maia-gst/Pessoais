import numpy as np
from numbers import Real
from numpy import array


def determinant(matrix: array) -> Real:
    reduced = row_reduce(matrix)
    result = 1
    for i in range(matrix.shape[1]):
        result *= reduced[i, i]
    return result


def row_reduce(a: array) -> array:
    matrix = np.copy(a).astype('float64')
    for column in range(matrix.shape[1]):
        for i in range(column + 1, matrix.shape[0]):
            if matrix[column, column] == 0:
                if all(matrix[:, column] != 0):
                    continue
                matrix[column] += matrix[column + np.argmax(matrix[column:, column] != 0)]
                if matrix[column, column] == 0:
                    matrix[i] -= matrix[i]
                    continue

            matrix[i] -= matrix[column] * matrix[i, column] / matrix[column, column]
    return matrix


def solve(a: array, b: array) -> array:
    n_rows, n_columns = a.shape
    if n_rows != n_columns:
        return None
    if determinant(a) == 0:
        raise ValueError("The matrix is singular, the only solution to the linear system ")

    augmented = np.concatenate((a, b), axis=1)
    reduced = row_reduce(augmented)

    for column in range(a.shape[1] - 1, 0, -1):
        if reduced[column, column] != 0:
            for i in range(column):
                reduced[i] -= reduced[column] * reduced[i, column] / reduced[column, column]

    for c in range(0, a.shape[0]):
        reduced[c] *= 1 / reduced[c, c]

    return reduced[:, -1]


if __name__ == '__main__':
    a = array([[2, 1, 1], [1, 1, 4], [0, 3, 2]])
    b = array([[8], [15], [9]])
    print(solve(a, b))
