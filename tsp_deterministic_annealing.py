from tsp_hillclimbing import get_neighbour, evaluate_function
import numpy as np

def deterministic_annealing(distances: np.ndarray, initial_route: list, t_init: float = 2000.0, alpha: float = 0.999, max_iter: int = 50000) -> tuple[list, float, list]:
    current_route = initial_route[:]
    current_score = evaluate_function(current_route, distances)

    best_route = current_route
    best_score = current_score
    history = [best_score]

    t = t_init

    for _ in range(max_iter):
        neighbor = get_neighbour(current_route)
        neighbor_score = evaluate_function(neighbor, distances)

        if neighbor_score - current_score <= t:
            current_route = neighbor
            current_score = neighbor_score

            if current_score < best_score:
                best_route = current_route[:]
                best_score = current_score
                history.append(best_score)

        t *= alpha

    return best_route, best_score, history