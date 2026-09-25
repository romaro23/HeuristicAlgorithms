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

def hill_climbing(distances: np.ndarray, initial_route: list, max_stuck: int = 500) -> tuple[list, float, list]:
    best_route = initial_route[:]
    best_score = evaluate_function(best_route, distances)
    history = [best_score]

    stuck_counter = 0

    while stuck_counter < max_stuck:
        next_route = get_neighbour(best_route)
        next_score = evaluate_function(next_route, distances)

        if next_score < best_score:
            best_route = next_route[:]
            best_score = next_score
            stuck_counter = 0
            history.append(next_score)
        else:
            stuck_counter += 1

    return best_route, best_score, history

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

