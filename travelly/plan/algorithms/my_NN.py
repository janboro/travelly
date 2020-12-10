def get_nearest_neighbour(matrix, visited, node):
    min = float("inf")
    min_index = -1

    for i in range(len(matrix)):
        if visited[i] == True or i == node:
            pass
        else:
            if matrix[node][i] < min:
                min = matrix[node][i]
                min_index = i
    return min_index, min


def solve(matrix, visited, path=[], node=0, cost=0):
    visited[node] = True
    path.append(node)
    if all(visited):
        return path, cost
    next_node, add_cost = get_nearest_neighbour(matrix, visited, node)
    cost += add_cost
    return solve(matrix, visited, path, next_node, cost)


def solve_my_NN(matrix):
    visited = [False] * len(matrix)
    path, cost = solve(matrix, visited)
    path.append(0)
    cost += matrix[path[-2]][path[-1]]
    return path, cost
