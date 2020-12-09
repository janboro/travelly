from utils import get_final_cost

def get_furthest_neighbour(matrix, visited, node):
    max = -1
    max_index = -1
    
    for i in range(len(matrix)):
        if visited[i] == True or i == node:
            pass
        else:
            if matrix[node][i] > max:
                max = matrix[node][i]
                max_index = i
    return max_index, max

def get_insertion_index(distance_matrix, path, visited, next_node):
    cost = float('inf')
    insert_index = int()
    for i in path:
        index = i
        if i == path[-1]:
            next_index = path[0]
        else:
            temp = path.index(index) + 1
            next_index = path[temp]

        current_cost = distance_matrix[index][next_node] +\
                        distance_matrix[next_node][next_index]-\
                        distance_matrix[index][next_index]

        if current_cost < cost:
            cost = current_cost
            insertion_index = path.index(index) + 1
    return insertion_index


def solve(matrix, visited, path=[], node=0):
    if all(visited):
        return path

    if node == 0 and not all(visited):
        path.append(node)
        visited[node] = True
        next_node, _ = get_furthest_neighbour(matrix, visited, node)
        path.append(next_node)
        
    else:
        maximum = -1
        next_node = int()
        for city in path:
            node_index, max = get_furthest_neighbour(matrix, visited, node)
            if max > maximum:
                maximum = max
                next_node = node_index
        insert_index = get_insertion_index(matrix, path, visited, next_node)
        path.insert(insert_index, next_node)
    visited[next_node] = True
    

    return solve(matrix, visited, path, next_node)


def solve_furthest_insertion(matrix):
    visited = [False] * (len(matrix))
    path = solve(matrix, visited)
    path.append(path[0])
    cost = get_final_cost(matrix, path)
    return path, cost