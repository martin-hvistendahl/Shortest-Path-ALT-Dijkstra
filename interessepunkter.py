import heapq
import pickle
from visualiser import visualiser_graf, hent_kordinat


# Laster inn grafen fra den serialiserte filen
with open('graf.pkl', 'rb') as f:
    graf = pickle.load(f)

def les_interessepunkter(filnavn):
    interessepunkter = {}
    
    with open(filnavn, 'r', encoding='utf-8') as fil:
        for linje in fil:
            deler = linje.strip().split(maxsplit=2)
            if len(deler) != 3:
                continue  # Hopper over linjer som ikke har tre deler

            nodenr, kode, navn = deler
            nodenr = int(nodenr)
            kode = int(kode)
            navn = navn.strip('"')  # Fjerner anførselstegn rundt navnet
            if kode & 2:
                interessepunkter[nodenr] = {'type': "bensinstasjon", 'navn': navn}
            if kode & 4:  # Ladestasjon
                interessepunkter[nodenr] = {'type': "ladestasjon", 'navn': navn}
            if kode & 8:  # Spisested
                interessepunkter[nodenr] = {'type': "spisested", 'navn': navn}
            if kode & 16: # Drikkested
                interessepunkter[nodenr] = {'type': "drikkested", 'navn': navn}
            if kode & 32: # Overnattingssted
                interessepunkter[nodenr] = {'type': "overnattingssted", 'navn': navn}
    return interessepunkter

def dijkstra_for_interessepunkter(graph, start, interessepunkter, max_antall, type):
    distances = {node: float('infinity') for node in graph}
    distances[start] = 0
    priority_queue = [(0, start)]
    funnet_interessepunkter = []
    
    
    while priority_queue and len(funnet_interessepunkter) < max_antall:
        current_distance, current_node = heapq.heappop(priority_queue)

        #hvis current_node finnes som index i interessepunkt og current_node ikke er i funnet_interessepunkter og interestpunktet type er ladestasjon
        if current_node in interessepunkter and current_node not in funnet_interessepunkter and interessepunkter[current_node]['type'] == type:
            funnet_interessepunkter.append(current_node)

        for neighbor, weight in graph.get(current_node, []):
            if neighbor not in distances:
                continue  # Hopper over noder som ikke er i grafen

            distance = current_distance + weight
            if distance < distances[neighbor]:
                distances[neighbor] = distance
                heapq.heappush(priority_queue, (distance, neighbor))

    return funnet_interessepunkter

noder=[2266026]
interessepunkter = les_interessepunkter('interessepkt.txt')
type= 'ladestasjon'
for node in noder:
    nærmeste_ladestasjon = dijkstra_for_interessepunkter(graf, node, interessepunkter, 5, type)
    kordinater=hent_kordinat(nærmeste_ladestasjon)
    visualiser_graf(kordinater,1, node, type) 