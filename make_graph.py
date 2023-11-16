import pickle
def les_graf(filnavn):
    with open(filnavn, 'r') as fil:
        antall_linjer = int(fil.readline().strip())  # Leser antall linjer

        graf = {}
        for _ in range(antall_linjer):
            
            fra_node, til_node, kjøretid, _, _ = map(int, fil.readline().split())
            
            if fra_node not in graf:
                graf[fra_node] = []
            
            # Legger til kanten i grafen
            graf[fra_node].append((til_node, kjøretid))

        return graf
graf = les_graf('kanter.txt')
# Lagrer grafen med pickle
with open('graf.pkl', 'wb') as f:
    pickle.dump(graf, f)
