import networkx as nx

red_line = [
    "Akademmistechko",
    "Zhytomyrska",
    "Sviatoshyn",
    "Nivky",
    "Beresteiska",
    "Shuliavska",
    "Polytechnichnyi Instytut",
    "Vokzalna",
    "Universytet",
    "Teatralna",
    "Khreshchatyk",
    "Arsenalna",
    "Dnipro",
    "Hydropark",
    "Livoberezhna",
    "Darnytsia",
    "Chernihivska",
    "Lisova",
]

blue_line = [
    "Heroiv Dnipra",
    "Minska",
    "Obolon",
    "Pochaina",
    "Tarasa Shevchenka",
    "Kontraktova Ploshcha",
    "Poshtova Ploshcha",
    "Maidan Nezalezhnosti",
    "Ploshcha Lva Tolstoho",
    "Olimpiiska",
    "Palats Ukraina",
    "Lybidska",
    "Demiivska",
    "Holosiivska",
    "Vasylkivska",
    "Vystavochnyi Tsentr",
    "Ipodrom",
    "Teremky",
]

green_line = [
    "Syrets",
    "Dorohozhychi",
    "Lukianivska",
    "Zoloti Vorota",
    "Palats Sportu",
    "Klovska",
    "Pecherska",
    "Druzhby Narodiv",
    "Vydubychi",
    "Slavutych",
    "Osokorky",
    "Pozniaky",
    "Kharkivska",
    "Boryspilska",
    "Vyrlytsia",
    "Chervony Khutir",
]

G = nx.Graph()


def add_line(stations: list[str], line_name: str) -> None:
    edges = [(stations[i], stations[i + 1]) for i in range(len(stations) - 1)]
    G.add_edges_from(edges, line=line_name)


add_line(red_line, "M1 (red)")
add_line(blue_line, "M2 (blue)")
add_line(green_line, "M3 (green)")

# пересадки
G.add_edges_from(
    [
        ("Teatralna", "Zoloti Vorota"),  # червона  зелена
        ("Khreshchatyk", "Maidan Nezalezhnosti"),  # червона синя
        ("Palats Sportu", "Ploshcha Lva Tolstoho"),  # зелена синя
    ],
    line="transfer",
)

#  Додаємо ваги

for _, _, data in G.edges(data=True):
    data["weight"] = 1  # 1 станція = 1 крок

graph = {u: {v: data["weight"] for v, data in G[u].items()} for u in G.nodes()}


def dijkstra(graph, start):
    distances = {vertex: float("infinity") for vertex in graph}
    distances[start] = 0
    unvisited = list(graph.keys())

    while unvisited:
        current_vertex = min(unvisited, key=lambda v: distances[v])
        if distances[current_vertex] == float("infinity"):
            break
        for neighbor, weight in graph[current_vertex].items():
            new_dist = distances[current_vertex] + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
        unvisited.remove(current_vertex)
    return distances


all_pairs_dist = {src: dijkstra(graph, src) for src in graph}

for src, dist_dict in all_pairs_dist.items():
    for dst, d in dist_dict.items():
        print(f"{src:20} -> {dst:20} : {int(d)}")

print("\nНайкоротша кількість станцій між вибраними парами:")
for a, b in [
    ("Heroiv Dnipra", "Lisova"),
    ("Syrets", "Teremky"),
    ("Universytet", "Maidan Nezalezhnosti"),
]:
    print(f"{a:>20} → {b:<20}: {int(all_pairs_dist[a][b])} станцій")
