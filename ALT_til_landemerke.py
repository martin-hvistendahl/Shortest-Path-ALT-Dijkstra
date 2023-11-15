import heapq
import pickle
import pandas as pd
import os

def dijkstra1(graph, start):
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

def omvend_graf(graph):
    omvendt = {}
    for node, edges in graph.items():
        if node not in omvendt:
            omvendt[node] = []
        for edge in edges:
            neighbor, weight = edge
            if neighbor not in omvendt:
                omvendt[neighbor] = []
            omvendt[neighbor].append((node, weight))
    return omvendt

def alt_preprosessering_til(graph, landemerke):
    avstand_til_landemerker = dijkstra1(graph, landemerke)
    return avstand_til_landemerker



landemerker = [918769]#, 894067, 5770561, 2438190, 412001, 5436444]
# Etter at du har kjørt alt_preprosessering
for landemerke in landemerker:
    file='fra_{landemerke}.pkl'.format(landemerke=landemerke)
    with open(file, 'rb') as f:
        graf = pickle.load(f)
    print(type(graf))  # Sjekk typen til graf
    print(list(graf.items())[:5])    
    omvendt_graph = omvend_graf(graf)
    avstand_til_landemerker = alt_preprosessering_til(omvendt_graph, landemerke)
    name='til_{landemerke}.pkl'.format(landemerke=landemerke)
    with open(name, 'wb') as f:
        pickle.dump(avstand_til_landemerker, f)
