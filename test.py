def multiply_matrix(a, b):
    matrix = []
    for k in range(len(a)):
        row = []
        for i in range(len(b)):
            value = 0
            for j in range(len(b)):
                value+= a[k][j] * b[j][i]
            row.append(value)
        matrix.append(row)
    return matrix


a = [[1, 0, 0], [0,1,0], [-4,-4,1]]

b = [
    [-1, 0, 0],
    [0, -1, 0],
    [0, 0, 1]
]

c = [
    [2, 0, 0], [0, 1, 0], [0, 0, 1]
]

d = [
    [1, 0, 0], [0, 1, 0], [8, 6, 1]
]

print(multiply_matrix(multiply_matrix(multiply_matrix(a,b),c),d))