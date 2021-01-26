final_matrix=[[3.57, 2.71, 9.2, 5.63],
              [4.42, 1.4, 3.53, 8.97],
              [1.2, 0.33, 6.26, 7.77],
              [6.36, 3.6, 8.91, 7.42],
              [1.59, 0.9, 2.4, 4.24]]

min_values = []
for i in range(3):
    mini = final_matrix[0][0]
    for row in final_matrix:
        for n in row:
            if n < mini:
                mini = n
                n_index = row.index(n)
                row_index = final_matrix.index(row)
    min_values.append(mini)
    del final_matrix[row_index][n_index]




print("Finals {}".format(min_values))
