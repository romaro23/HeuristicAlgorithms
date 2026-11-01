import numpy as np
import math
import random
import numpy

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

# def hill_climbing(distances: np.ndarray, initial_route: list) -> tuple[list, float, list]:
#     best_route = initial_route[:]
#     best_score = evaluate_function(best_route, distances)
#     history = [best_score]
#
#     improved = True
#
#     while improved:
#         improved = False
#         current_best_neighbor = best_route
#         current_best_score = best_score
#
#         n = len(best_route)
#
#         for i in range(n - 1):
#             for j in range(i + 1, n):
#                 neighbor = best_route[:i] + best_route[i:j][::-1] + best_route[j:]
#                 neighbor_score = evaluate_function(neighbor, distances)
#
#                 if neighbor_score < current_best_score:
#                     current_best_score = neighbor_score
#                     current_best_neighbor = neighbor
#
#         if current_best_neighbor is not None:
#             best_route = current_best_neighbor
#             best_score = current_best_score
#             history.append(best_score)
#             improved = True
#
#     return best_route, best_score, history

def hill_climbing(distances: np.ndarray, initial_route: list) -> tuple[list, float, list]:
    best_route = initial_route[:]
    best_score = evaluate_function(best_route, distances)
    history = [best_score]

    n = len(best_route)
    improved = True

    while improved:
        improved = False
        best_delta = 0.0
        best_i, best_j = 0, 0

        for i in range(1, n - 1):
            for j in range(i + 1, n + 1):
                n1 = best_route[i - 1]
                n2 = best_route[i]
                n3 = best_route[j - 1]
                n4 = best_route[j % n]

                d_broken = distances[n1][n2] + distances[n3][n4]
                d_new = distances[n1][n3] + distances[n2][n4]

                delta = d_new - d_broken

                if delta < best_delta:
                    best_delta = delta
                    best_i = i
                    best_j = j

        if best_delta < -1e-5:
            best_route = best_route[:best_i] + best_route[best_i:best_j][::-1] + best_route[best_j:]
            best_score += best_delta
            history.append(best_score)
            improved = True

    final_score = evaluate_function(best_route, distances)
    history[-1] = final_score

    return best_route, final_score, history

def multi_start_hill_climbing(distances: np.ndarray, num_starts: int = 100) -> tuple[list, float, list]:
    all_scores = []
    n = len(distances)

    best_route = list(range(n))
    best_score = float('inf')

    for _ in range(num_starts):
        initial_route = list(range(n))
        random.shuffle(initial_route)

        route, score, _ = hill_climbing(distances, initial_route)
        all_scores.append(score)

        if score < best_score:
            best_route = route[:]
            best_score = score

    return best_route, best_score, all_scores

