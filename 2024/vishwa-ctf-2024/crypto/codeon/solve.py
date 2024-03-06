import numpy as np

matrix_a = np.array([
    [45, 35, 93, 95, 24, 65],
    [25, 15, 55, 64, 36, 45],
    [15, 65, 62, 16, 65, 38],
    [19, 64, 35, 69, 65, 63],
    [47, 67, 48, 60, 39, 27],
    [66, 48, 77, 22, 10, 69]
])

matrix_b = np.array([
    [33, 25, 30, 11, 68, 65],
    [83, 36, 19, 33, 55, 51],
    [20, 16, 48, 63, 41, 71],
    [30, 42, 12, 25, 31, 37],
    [51, 3, 44, 23, 43, 85],  
    [20, 39, 28, 41, 1, 70]   
])

matrix_elementwise_product = matrix_a * matrix_b
matrix_result_mod = np.mod(matrix_result, 118)
print(matrix_result_mod)
