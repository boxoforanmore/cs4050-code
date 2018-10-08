def connected(matrix, n=4):
    if n == 1:
        return True
    else:
        if not connected(matrix[:n-1][:n-1], n-1):
            return False
        else:
            for j in range(n-1):
                if matrix[n-1][j] == 1:
                    return True
        return False
'''
mat = \
[[0, 1, 1, 0],
 [1, 0, 0, 0],
 [1, 0, 0, 0],
 [0, 0, 0, 0]]
'''
'''
mat = [[0, 1, 0, 1, 0, 1],
       [1, 0, 1, 0, 1, 0], 
       [0, 1, 0, 0, 1, 0],
       [1, 0, 0, 0, 0, 0],
       [0, 1, 1, 0, 0, 0],
       [1, 0, 0, 0, 0, 0]]
'''

'''
mat = [[0, 1, 0],
       [1, 0, 1],
       [0, 1, 0]]
'''

mat = [[1, 0, 0],
       [0, 1, 0],
       [0, 0, 1]]
print(connected(mat, len(mat)))
