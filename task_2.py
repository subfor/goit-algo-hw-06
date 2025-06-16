from collections import deque
from typing import Any, Dict

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


def dfs_path(graph, start, goal):
    stack = [(start, [start])]
    visited = set()
    while stack:
        vertex, path = stack.pop()
        if vertex == goal:
            return path
        if vertex in visited:
            continue
        visited.add(vertex)
        for nbr in reversed(list(graph.neighbors(vertex))):
            if nbr not in visited:
                stack.append((nbr, path + [nbr]))
    return []


def bfs_path(graph, start, goal):
    queue = deque([(start, [start])])
    visited = {start}
    while queue:
        vertex, path = queue.popleft()
        if vertex == goal:
            return path
        for nbr in graph[vertex]:
            if nbr not in visited:
                visited.add(nbr)
                queue.append((nbr, path + [nbr]))
    return []


# Tests
pairs = [
    ("Akademmistechko", "Lisova"),
    ("Heroiv Dnipra", "Lisova"),
    ("Syrets", "Teremky"),
]

for src, dst in pairs:
    p_dfs = dfs_path(G, src, dst)
    p_bfs = bfs_path(G, src, dst)

    print(f"\n{src} → {dst}")
    print("DFS:", " → ".join(p_dfs), f"(довжина {len(p_dfs)-1})")
    print("BFS:", " → ".join(p_bfs), f"(довжина {len(p_bfs)-1})")
    if len(p_dfs) != len(p_bfs):
        print("   ⚠ BFS найкоротший; DFS може бути довшим через інший порядок обходу")


"""
DFS vs BFS (Kyiv-metro)

• Akademmistechko → Lisova  – 17 ребер у обох.
  Лише пряма червона лінія, альтернатив немає.

• Heroiv Dnipra → Lisova   – DFS 19 > BFS 15.
  DFS зайшов через Palats Sportu - Zoloti Vorota (довший обхід),
  BFS одразу взяв коротшу пересадку Maidan - Khreshchatyk.

• Syrets → Teremky         – 14 ребер у обох.
  Єдиний мінімальний шлях із зеленої на синю через
  Palats Sportu ↔ Ploshcha Lva Tolstoho; DFS випадково потрапив у нього.
"""
