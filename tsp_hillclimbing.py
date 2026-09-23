import numpy as np
import math
import random
import copy
import numpy
import tsplib95


def calculate_distances(coords: list[tuple[float, float]], n: int) -> np.ndarray:
    matrix = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            x1, y1 = coords[i]
            x2, y2 = coords[j]

            dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
            matrix[i][j] = dist

    return matrix

def evaluate_function(route: list, distances: np.ndarray) -> float:
    total_dist = 0

    for i in range(len(route) - 1):
        current_city = route[i]
        next_city = route[i + 1]
        total_dist += distances[current_city][next_city]

    total_dist += distances[route[-1]][route[0]]

    return total_dist

def get_neighbour(route: list) -> list:
    i, j = sorted(random.sample(range(len(route)), 2))
    return route[:i] + route[i:j][::-1] + route[j:]

def hill_climbing(distances: np.ndarray, initial_route: list, max_stuck: int = 500) -> tuple[list, float]:
    best_route = initial_route[:]
    best_score = evaluate_function(best_route, distances)

    stuck_counter = 0

    while stuck_counter < max_stuck:
        next_route = get_neighbour(best_route)
        next_score = evaluate_function(next_route, distances)

        if next_score < best_score:
            best_route = next_route[:]
            best_score = next_score
            stuck_counter = 0
        else:
            stuck_counter += 1

    return best_route, best_score

filepath = r"D:\PycharmProjects\University\HeuristicAlgorithms\data\berlin52.tsp"
problem = tsplib95.load(filepath)

cities = list(problem.node_coords.values())
N = problem.dimension

distances = calculate_distances(cities, N)

test_list = list(range(52))
random.shuffle(test_list)
print(hill_climbing(distances, test_list))
