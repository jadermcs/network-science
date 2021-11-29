import re
import csv
import json
import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict

with open("ancestry.json") as fin:
    mapping = json.load(fin)

def main():
    g = nx.Graph()
    comm = set()
    dise = set()
    count = 0
    with open("data.tsv") as fin:
        data = csv.DictReader(fin, delimiter='\t')
        for row in data:
            count +=1
            pattern = r"[A-Za-z]+[A-Za-z\s\,]+ancestry"
            match = re.findall(pattern, row['INITIAL SAMPLE SIZE']) +\
                re.findall(pattern, row['REPLICATION SAMPLE SIZE'])
            disease = row['MAPPED_TRAIT']
            dise.add(disease)
            origins = set()
            for m in match:
                for continent, naming in mapping.items():
                    for name in naming:
                        if name in m:
                            origins.add(continent)
            for continent in origins:
                comm.add(continent)
                g.add_edge(continent, disease)
    # Compute statistics
    print("Node count")
    for n in g.degree:
        if n[0] in mapping:
            print(n)
    print("Average path length")
    print(nx.average_shortest_path_length(g))
    print("Average clustering")
    print(nx.average_clustering(g))
    print("Degree correlation")
    print(nx.degree_pearson_correlation_coefficient(g))
    # Plot distribution statistics
    counter = defaultdict(int)
    for d in g.degree():
        if d[1] == 0: continue
        counter[d[1]] += 1
    nodes = len(g.nodes())
    k = [k[0] for k in counter.items()]
    pk = [k[1]/nodes for k in counter.items()]
    plt.xscale('log')
    plt.yscale('log')
    plt.title('Degree Distribution log-log')
    plt.xlabel('<k> (log)')
    plt.ylabel('$p_k$ (log)')
    plt.scatter(k, pk, label='probability of <k>')
    plt.savefig("continent-distribution.png", dpi=300, transparent=True)
    plt.show()
    # Plot bipartite network
    pos = dict()
    pos.update((n, (1, i*900)) for i, n in enumerate(comm))
    pos.update((n, (2, i)) for i, n in enumerate(dise))
    for i, c in enumerate(comm):
        plt.text(1, i*900+180, c, horizontalalignment='center')
    nx.draw(g, pos=pos, with_labels=False, width=.25, edge_color=(0,0,0,.25))
    plt.title("Bipartite graph of Continents and Studied Diseases")
    plt.savefig("continent-bipartite.png", dpi=300, transparent=True)
    plt.show()
    # Robustness
    components = []
    for i in range(1000):
        comps = nx.number_connected_components(g)
        components.append(comps)
        max_node = max(list(g.degree()), key=lambda x: x[1])[0]
        g.remove_node(max_node)
    plt.title("Number of components after remove N nodes")
    plt.xlabel("N# of nodes removed")
    plt.ylabel("N# of components")
    plt.plot(range(len(components)), components, '^k:')
    plt.savefig("components.png", dpi=300, transparent=True)
    plt.show()


if __name__ == "__main__":
    main()
