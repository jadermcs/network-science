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
            for m in match:
                comm.add(m)
                g.add_edge(m, disease)
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
    plt.savefig("distribution.png", dpi=300, transparent=True)
    plt.show()
    # Plot bipartite network
    pos = dict()
    pos.update((n, (1, i*10)) for i, n in enumerate(comm))
    pos.update((n, (2, i)) for i, n in enumerate(dise))
    nx.draw(g, pos=pos, with_labels=False, width=.25, edge_color=(0,0,0,.25))
    plt.title("Bipartite graph of Communities and Studied Diseases")
    plt.savefig("bipartite.png", dpi=300, transparent=True)
    plt.show()

if __name__ == "__main__":
    main()
