from typing import Any, Dict

import matplotlib.pyplot as plt
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

print(f"Станцій: {G.number_of_nodes()}")
print(f"Ребер (з переходами): {G.number_of_edges()}")
deg: Dict[Any, int] = {n: d for n, d in G.degree()}

print(f"Середній ступінь: {sum(deg.values())/len(deg):.2f}")
print("Пересадочні вузли (ступінь > 2):", [v for v, d in deg.items() if d > 2])

colors = {
    "M1 (red)": "#d73027",
    "M2 (blue)": "#4575b4",
    "M3 (green)": "#1a9850",
    "transfer": "#999999",
}
pos = nx.kamada_kawai_layout(G)

plt.figure(figsize=(12, 9))


for line, col in colors.items():
    edgelist = [(u, v) for u, v, data in G.edges(data=True) if data["line"] == line]
    nx.draw_networkx_edges(G, pos, edgelist=edgelist, width=2, edge_color=col)

nx.draw_networkx_nodes(G, pos, node_size=500, node_color="#ffffff", edgecolors="black")
nx.draw_networkx_labels(G, pos, font_size=7)

plt.title("Kyiv Metro – M1 (red), M2 (blue), M3 (green)")
plt.axis("off")
plt.tight_layout()
plt.show()
