import heapq
import pandas as pd
import pickle

with open('graf.pkl', 'rb') as f:
    graf = pickle.load(f)
# Load the precomputed distances from the CSV files
def load_precomputed_distances(landmarks):
    distances_from = {}
    distances_to = {}
    for landmark in landmarks:
        distances_from[landmark] = pd.read_csv(f'fra_{landmark}.csv', index_col=0)
        distances_to[landmark] = pd.read_csv(f'til_{landmark}.csv', index_col=0)
    return distances_from, distances_to

# Heuristic function for the A* search that uses landmark distances
def heuristic(node, goal, distances_from, distances_to):
    # Use the triangle inequality to compute the heuristic
    h = 0
    for landmark in distances_from:
        # Ensure you are getting a single value from the DataFrame, not a Series
        pi_s = distances_from[landmark].loc[node].item()
        pi_t = distances_to[landmark].loc[goal].item()
        h = max(h, abs(pi_s - pi_t))
    return h


# A* search algorithm
def a_star_search(graph, start, goal, distances_from, distances_to):
    priority_queue = [(0 + heuristic(start, goal, distances_from, distances_to), 0, start)]
    came_from = {start: None}
    cost_so_far = {start: 0}
    behandlet_noder = 0  # Processed nodes counter

    while priority_queue:
        _, current_cost, current = heapq.heappop(priority_queue)
        behandlet_noder += 1  # Increment the counter for each node removed from the queue

        if current == goal:
            break  # Found the goal
        
        for neighbor, weight in graph.get(current, []):
            new_cost = current_cost + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                priority = new_cost + heuristic(neighbor, goal, distances_from, distances_to)
                heapq.heappush(priority_queue, (priority, new_cost, neighbor))
                came_from[neighbor] = current

    # Reconstruct path
    path = []
    node = goal
    while node is not None:
        path.append(node)
        node = came_from[node]
    path.reverse()  # optional, if you want the path from start to goal

    return cost_so_far, path, behandlet_noder

# Main execution
landemerker = [918769, 894067, 5770561, 2438190, 412001, 5436444]
distances_from, distances_to = load_precomputed_distances(landemerker)

# Run the A* search algorithm with the ALT heuristic
start_node = 6441311  # Replace with actual start node
goal_node = 3168086   # Replace with actual goal node
shortest_distances, path, behandlet_noder = a_star_search(graf, start_node, goal_node, distances_from, distances_to)

# Calculate time assuming shortest_distances[end_node[i]] is in tenths of seconds
tid = shortest_distances[goal_node] / 100
timer = int(tid // 3600)
minutter = int((tid % 3600) // 60)
sekunder = int(tid % 60)
tid_formatert = f"{timer:02d}:{minutter:02d}:{sekunder:02d}"

print(f"Path from {start_node} to {goal_node}: {len(path)}")
print(f"Total nodes processed: {behandlet_noder}")
print(f"Formatted time: {tid_formatert}")
