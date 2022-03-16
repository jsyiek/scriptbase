import csv

from typing import Dict, List, Set, Tuple, Union

def get_csv_contents(csv_path: str) -> List[List]:
    """
    Reads the contents from a csv and returns the results

    Parameters:
        csv_path (str): Path to CSV

    Returns:
        List[List]: List of lists, with each sub-list corresponding to a row of the CSV
    """

    with open(csv_path, "r") as F:

        csv_file = csv.reader(F)

        return [line for line in csv_file]


def compute_max_flow(capacity, s, t):
    flow_graph = {edge: [0, cap] for edge, cap in capacity.items()}
    residual_graph = generate_residual_graph(flow_graph)
    augmenting_path, cutset = breadth_first_search(residual_graph, s, t)
    while augmenting_path is not None:
        amount_to_change = min(flow_graph[(u, v)][1] - flow_graph[(u, v)][0] if dire == 1
                               else flow_graph[(v, u)][0]
                               for (u, v, dire) in augmenting_path)
        for u, v, dire in augmenting_path:
            if dire == 1:
                flow_graph[(u, v)][0] += amount_to_change
            else:
                flow_graph[(v, u)][0] -= amount_to_change
        residual_graph = generate_residual_graph(flow_graph)
        augmenting_path, cutset = breadth_first_search(residual_graph, s, t)

    flow = {}
    flow_value = 0
    for edge in flow_graph:
        if edge[-1] == t:
            flow_value += flow_graph[edge][0]
        flow[edge] = flow_graph[edge][0]

    generate_residual_graph(flow_graph)
    return flow_value, flow, cutset


def generate_residual_graph(current_capacities: Dict[Tuple[int, int], List[int]]) -> Dict[int, Set[int]]:
    residual_graph = {}

    for (s, t), (curr_cap, max_cap) in current_capacities.items():
        if max_cap >= curr_cap > 0:
            residual_graph.setdefault(t, set()).add((s, -1))
        if curr_cap < max_cap:
            residual_graph.setdefault(s, set()).add((t, 1))
    return residual_graph


def breadth_first_search(graph, s, t):
    Q = [[(s, s, 1)]]
    visited = set()
    while Q:
        path = Q.pop(0)
        _, n, __ = path[-1]
        if n in visited:
            continue
        visited.add(n)
        if (t, 1) in graph.get(n, set()):
            path.append((n, t, 1))
            return path[1:], None
        elif (t, -1) in graph.get(n, set()):
            path.append((n, t, -1))
            return path[1:], None
        for v, dire in graph.get(n, set()):
            Q.append(path + [(n, v, dire)])
    return None, visited


if __name__ == "__main__":

    for filepath in ["flownetwork_00.csv", "flownetwork_01.csv", "flownetwork_02.csv"]:
        capacity = {
            (int(u), int(v)): int(edge_capacity) for (u, v, edge_capacity) in get_csv_contents(filepath)[1:]
        }
        unweighted_graph = {}
        for u, v in capacity:
            unweighted_graph.setdefault(u, set()).add(v)
        # print(breadth_first_search(unweighted_graph, 1, 5))
        if "00" in filepath:
            print(compute_max_flow(capacity, 0, 3))
        elif "01" in filepath:
            print(compute_max_flow(capacity, 0, 2))
        else:
            print(compute_max_flow(capacity, 0, 5))
