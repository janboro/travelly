import tspsolve
import numpy as np
from travelly.plan.utils import get_final_cost


def solve_nn(matrix):
    path = list(tspsolve.nearest_neighbor(np.matrix(matrix)))
    path.append(path[0])
    cost = get_final_cost(matrix, path)
    return path, cost
