import re
import csv
import json
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

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
            match = re.findall(pattern, row['INITIAL SAMPLE SIZE'])
            # match2 = re.findall(pattern, row['REPLICATION SAMPLE SIZE'])
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
    pos = dict()
    pos.update((n, (1, i*900)) for i, n in enumerate(comm))
    pos.update((n, (2, i)) for i, n in enumerate(dise))
    for i, c in enumerate(comm):
        plt.text(1, i*900+180, c, horizontalalignment='center')
    nx.draw(g, pos=pos, with_labels=False, width=.25, edge_color=(0,0,0,.25))
    plt.title("Bipartite graph of Communities and Studied Diseases")
    plt.savefig("bipartite.png", dpi=300, transparent=True)
    print(g)

if __name__ == "__main__":
    main()
