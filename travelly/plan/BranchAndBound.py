maxsize = float("inf")
final_path = list()
N = int()
final_solution = maxsize


def temp_to_final_solution(temp_path):
    final_path[: N + 1] = temp_path[:]
    final_path[N] = temp_path[0]


def first_minimum_edge(matrix, i):
    min = maxsize
    for j in range(N):
        if matrix[i][j] < min and i != j:
            min = matrix[i][j]
    return min


def second_minimum_edge(matrix, i):
    first, second = maxsize, maxsize
    for j in range(N):
        if i == j:
            continue
        if matrix[i][j] <= first:
            second = first
            first = matrix[i][j]
        elif matrix[i][j] <= second and matrix[i][j] != first:
            second = matrix[i][j]
    return second


def b_n_b_reccurrent(matrix, temp_bound, temp_weight, level, temp_path, visited):
    """
    matrix -> matrix of costs
    temp_bound -> lower bound of root node
    temp_weigh -> weight of path so far
    level -> current level in tree
    temp_path[] -> solution beeing stored in temp
    visited[] -> Boolean of whether a node has been visited
    """
    global final_solution

    # case when we reach the bottom of the tree
    if level == N:
        # cheching if there is a path between last vertex to first vertex
        if matrix[temp_path[level - 1]][temp_path[0]] != 0:
            temp_solution = temp_weight + matrix[temp_path[level - 1]][temp_path[0]]
            # upgrading final solutioin with new, better solution
            if temp_solution < final_solution:
                temp_to_final_solution(temp_path)
                final_solution = temp_solution
        return

    # cases when we haven't reached the bottom of the tree
    # here we're building the tree recursively
    for i in range(N):
        if matrix[temp_path[level - 1]][i] != 0 and visited[i] == False:
            temp = temp_bound
            temp_weight += matrix[temp_path[level - 1]][i]

            if level == 1:
                temp_bound -= (
                    first_minimum_edge(matrix, temp_path[level - 1])
                    + first_minimum_edge(matrix, i)
                ) / 2
            else:
                temp_bound -= (
                    second_minimum_edge(matrix, temp_path[level - 1])
                    + first_minimum_edge(matrix, i)
                ) / 2

            # if current lower bound is lower than final lower bound
            lower_bound = temp_bound + temp_weight
            if lower_bound < final_solution:
                temp_path[level] = i
                visited[i] = True

                # calling the bnb recurrent algorythm to calculate next level
                b_n_b_reccurrent(
                    matrix, temp_bound, temp_weight, level + 1, temp_path, visited
                )

            temp_weight -= matrix[temp_path[level - 1]][i]
            temp_bound = temp

            visited = [False] * len(visited)
            for j in range(level):
                if temp_path[j] != -1:
                    visited[temp_path[j]] = True


def TSP_bnb(matrix):
    global N
    global final_path
    N = len(matrix)
    final_path = [None] * (N + 1)
    temp_bound = 0
    temp_path = [-1] * (N + 1)
    visited = [False] * N

    # calculating initial bound
    for i in range(N):
        temp_bound += first_minimum_edge(matrix, i) + second_minimum_edge(matrix, i)

    # temp_bound = math.ceil(temp_bound / 2)
    temp_bound /= 2

    # starting the path at index 0
    visited[0] = True
    temp_path[0] = 0

    b_n_b_reccurrent(
        matrix=matrix,
        temp_bound=temp_bound,
        temp_weight=0,
        level=1,
        temp_path=temp_path,
        visited=visited,
    )
    return final_path, final_solution
