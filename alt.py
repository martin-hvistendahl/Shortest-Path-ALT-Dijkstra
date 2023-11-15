import heapq
import pickle

# Laster inn grafen fra den serialiserte filen
with open('graf.pkl', 'rb') as f:
    graf = pickle.load(f)

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


def alt_preprosessering(graph, landemerke):
    avstand_fra_landemerker = {landemerke: dijkstra1(graph, landemerke) }
    #omvendt_graph = omvend_graf(graph)
    #avstand_til_landemerker = {node: dijkstra2(omvendt_graph, node, landemerke) for node in graph}

    # Lagre avstandstabellene til fil eller returner dem
    return avstand_fra_landemerker
    #return avstand_fra_landemerker, avstand_til_landemerker

# Eksempel på bruk
landemerker = [918769]#, 894067, 5770561, 2438190, 412001, 5436444]
import pandas as pd

def konverter_til_pandas_dataframe(graph, avstand_fra_landemerker):
    df = pd.DataFrame.from_dict(avstand_fra_landemerker, orient='index', columns=graph.keys())
    return df

# Etter at du har kjørt alt_preprosessering
avstand_fra_landemerker = alt_preprosessering(graf, landemerker[0])
df = konverter_til_pandas_dataframe(graf, avstand_fra_landemerker)
df.to_csv('avstand_fra_landemerker.csv')

# for landemerke in landemerker:
#     avstand_fra_landemerker = alt_preprosessering(graf, landemerke)
#    # avstand_fra_landemerker, avstand_til_landemerker = alt_preprosessering(graf, landemerke)
    
#     with open('avstand_fra_landemerker_{landemerke}.pkl', 'wb') as f:
#         pickle.dump(avstand_fra_landemerker, f)


