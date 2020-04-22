import networkx
import matplotlib.pyplot as plt

infections = open("../total_infections.dedupe5.log", "r")
act_infections = [inf.strip().split("\t") for inf in infections.readlines()]
print(len(act_infections), "infections loaded")

infs = set()
for inf in act_infections:
    if inf[1] not in infs:
        infs.add(inf[1])
    else:
        print("DUPE!")
        print(inf)
        exit()

print("No dupes")
infs = set()
infs.add("u/woodendoors7")
for inf in act_infections[1:]:
    infs.add(inf[1])
    if inf[3] not in infs:
        print("No record for", inf[3])
        exit()
print("No forest")

g = networkx.DiGraph()
g.add_node(act_infections[0][1])

for inf in act_infections[1:]:
    g.add_node(inf[1])
    g.add_edge(inf[3], inf[1])

print(networkx.is_directed_acyclic_graph(g))
