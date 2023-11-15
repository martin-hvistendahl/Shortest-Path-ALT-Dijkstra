import heapq
import pickle
from visualiser import visualiser_graf, hent_kordinat


# Laster inn grafen fra den serialiserte filen
with open('graf.pkl', 'rb') as f:
    graf = pickle.load(f)


def dijkstra_til_node(graph, start, goal):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    predecessors = {node: None for node in graph}
    behandlet_noder = 0  # Teller for antall noder behandlet

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        behandlet_noder += 1  # Inkrementerer telleren for hver node fjernet fra køen

        if current_node == goal:
            break

        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in distances:
                continue

            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                predecessors[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    # Rekonstruerer den korteste veien baklengs fra målet
    path = []
    if goal in predecessors:
        while goal is not None:
            path.insert(0, goal)
            goal = predecessors[goal]

    return distances, path, behandlet_noder


    

start_node = [2800567]#, 7705656, 647826, 136530, 7826348, 2948202, 339910, 1853145, 2503331, 2866570, 6441311, 3168086]
end_node = [7705656]#, 2800567, 136530, 647826, 2948202, 7826348, 1853145 , 339910, 2866570, 2503331,3168086 , 6441311]

for i in range(len(start_node)):
    shortest_distances, path, behandlet_noder = dijkstra_til_node(graf, start_node[i], end_node[i])
    
    tid = shortest_distances[end_node[i]] / 100
    timer = int(tid // 3600)
    minutter = int((tid % 3600) // 60)
    sekunder = int(tid % 60)
    tid_formatert = f"{timer:02d}:{minutter:02d}:{sekunder:02d}"

    kordinater=hent_kordinat(path)
    visualiser_graf(kordinater,0, start_node[i], end_node[i])
    
    print(f"Korteste vei fra {start_node[i]} til {end_node[i]} er {len(path)} noder lang og tar {tid_formatert}. Antall behandlet noder: {behandlet_noder}")


