import heapq
import pickle
import pandas as pd
import os

with open('graf.pkl', 'rb') as f:
    graf = pickle.load(f)

def dijkstra2(graph, start, goal):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)
        if current_node == goal:
            break
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
        # Legger til noden i omvendt, om den ikke allerede er der
        if node not in omvendt:
            omvendt[node] = []

        for neighbor, weight in edges:
            # Legger til nabo-noden i omvendt, om den ikke allerede er der
            if neighbor not in omvendt:
                omvendt[neighbor] = []
            omvendt[neighbor].append((node, weight))

    return omvendt

def lagre_avstand_til_fil(avstand_til_landemerke, landemerke, filnavn):
    df = pd.DataFrame.from_dict(avstand_til_landemerke, orient='index', columns=[landemerke])
    df.to_csv(f'{filnavn}_{landemerke}.csv', index_label='Node')

def alt_preprosessering_til_landemerker(omvendt_graph, landemerker, filnavn, write_every=100):
    node_counter = 0
    for landemerke in landemerker:
        avstand_til_landemerke = {}
        for node in omvendt_graph:
            avstand_til_landemerke[node] = dijkstra2(omvendt_graph, node, landemerke)
            node_counter += 1
            if node_counter % write_every == 0:
                lagre_avstand_til_fil(avstand_til_landemerke, landemerke, filnavn)
                avstand_til_landemerke = {}  # Nullstill dataen for neste runde
        lagre_avstand_til_fil(avstand_til_landemerke, landemerke, filnavn)

omvendt_graph = omvend_graf(graf)
alt_preprosessering_til_landemerker(omvendt_graph, [918769], "avstand_til", write_every=1)
