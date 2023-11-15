import gmplot

def hent_kordinat(noder):
    node_koordinater = {}
    with open("noder.txt", 'r', encoding='utf-8') as fil:
        next(fil)  # Hopper over den første linjen
        for linje in fil:
            deler = linje.strip().split()
            if len(deler) == 3:
                nodenr, lat, lon = deler
                node_koordinater[int(nodenr)] = (float(lat), float(lon))
                
    kordinater = []
    for node in noder:
        if node in node_koordinater:
            kordinater.append(node_koordinater[node])
    return kordinater
                     
def visualiser_graf(kordinater,number, start, slutt):
    gmap = gmplot.GoogleMapPlotter(kordinater[0][0], kordinater[0][1], 100)  # 13 er zoom-nivået

    
    if (number == 1):
        gmap.scatter(*zip(*kordinater), color='red', size=100, marker=False)

    else:
        gmap.scatter(*zip(*kordinater), color='red', size=100, marker=False)
        gmap.plot(*zip(*kordinater), 'cornflowerblue', edge_width=3)
   
    # Lagre kartet til en HTML-fil

    name=f"{start} til {slutt}.html"
    #make navn to a string
    
    gmap.draw(name) 