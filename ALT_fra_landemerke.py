import heapq
import pickle
import pandas as pd

# Laster inn grafen fra den serialiserte filen
with open('graf.pkl', 'rb') as f:
    graf = pickle.load(f)

def dijkstra(graph, start):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node not in graph:
            continue  # Hopper over noder som ikke er i grafen

        for neighbor, weight in graph[current_node]:
            if neighbor not in distances:
                continue  # Hopper over naboer som ikke er i distances-ordboken

            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return distances


def alt_preprosessering_fra(graph, landemerke):
    avstand_fra_landemerker = dijkstra(graph, landemerke)

    return avstand_fra_landemerker

landemerker = [918769]#, 894067, 5770561, 2438190, 412001, 5436444]


# Etter at du har kjørt alt_preprosessering
for landemerke in landemerker:
    avstand_fra_landemerker = alt_preprosessering_fra(graf, landemerke)
    name='fra_{landemerke}.pkl'.format(landemerke=landemerke)
    df_til = pd.DataFrame.from_dict(avstand_fra_landemerker)
    df_til.to_pickle(name)
    
    
    


