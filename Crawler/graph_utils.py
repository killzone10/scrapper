import networkx as nx
from write_edgelist_fixed import write_edgelist

def combineGraphs(G1, G2): ## polacz grafy
    G1.update(G2)
    G1.remove_edges_from(nx.selfloop_edges(G1)) ## usun duplikaty
    
def save_graph_gexf(G, filepath = "./", filename="graph.gexf"):
     nx.write_gexf(G, f"{filepath}{filename}") ## save graf gexf
    
def save_graph(G, filepath = "./", filename="graph.edgelist", delimiter= '<---->'): ## save
    write_edgelist(G, f"{filepath}{filename}", delimiter= delimiter, encoding='utf-8', comments=None)
    
    
def read_graph(filepath = "./", filename="graph.edgelist", nodetype=None, delimiter= '<---->',): ## sczytaj graf
    return nx.read_edgelist(f"{filepath}{filename}", nodetype=nodetype, create_using=nx.DiGraph, delimiter= delimiter, encoding='utf-8', comments=None)

