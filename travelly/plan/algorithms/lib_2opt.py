from py2opt.routefinder import RouteFinder


def solve_2opt(matrix):
    names = range(0, len(matrix))
    route_finder = RouteFinder(matrix, names)
    cost, path = route_finder.solve()
    path.append(path[0])
    cost += matrix[path[-2]][path[-1]]

    return path, cost
