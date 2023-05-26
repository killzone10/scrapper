import networkx as nx
from math import pow
import numpy as np
import json 
import matplotlib.pyplot as plt

'''Klasa slużąca analizie grafu, posiada funkcje potrzebne do analizy. Oprócz tego plotuje wykresy'''
class GraphAnaliser:
    def __init__(self, G, graph_name = 'graph'):
        self.G = G
        self.graph_name = graph_name
    
    def draw_graph(self, graph, name = 'graph.png', filepath = 'results/'): ##  narysuj graf i zapisz
        degrees = nx.degree(graph)
        degree_value = [n[-1] for n in degrees]
        degree_key = [n[0] for n in degrees]

        pos = nx.spring_layout(graph, seed = 123)
        plt.clf()
        plt.figure()
        plt.title(f"{self.graph_name}_{name}")
        nx.draw(graph, nodelist=degree_key, node_size=[v * 10 for v in degree_value], pos = pos)
        plt.savefig(f"{filepath}{self.graph_name}_{name}") 

    def draw(self, name = "graph.png", filepath = 'results/'):
        self.draw_graph(self.G, name = name, filepath = filepath) ## naryuj graf

    def print_graph_info(self):
        nodes = self.G.number_of_nodes() 
        edges = self.G.number_of_edges()
        print(f"Nodes (degree): {nodes}") ###rząd
        print(f"Edges (size): {edges}") ###rozmiar
        return nodes, edges
    
    def biggest_connected_component(self):    ## wyodrebnij najwieksza skladowa spojna
        UG = self.G.copy().to_undirected()
        largest_cc = max(nx.connected_components(UG), key=len)
        return UG.subgraph(largest_cc).copy()

    def weakly_connected_component(self): ## zwroc weakly_conn_comp
        comp = nx.weakly_connected_components(self.G)
        return comp

    def calculate_degrees(self): ## zwroc stopien
        degrees = nx.degree(self.G)
        degree_value = [n[-1] for n in degrees]
        return degree_value
    # średni stopień wierzchołka; 
    def calculate_mean_degree(self, degree_value): # zwroc sredni stopien 
        return sum(degree_value)/len(degree_value)  

    def plot_degree_distribution(self, degree_value, filepath = 'results/', name = 'degree_dst.png'): ## wyrysuj rozklad stopni grafu
        plt.clf()
        plt.hist(degree_value)
        plt.xlabel('Degree value')
        plt.ylabel('Degree count')
        plt.savefig(f"{filepath}{self.graph_name}_{name}")
    # średnica;
    def calculate_diameter(self): ## wylicz średnice
        try:
            return nx.diameter(self.G)
        except nx.NetworkXError:
            return 'inf'

     # promień;
    def calculate_radius(self): ## wylicz promień
        try:
            return nx.radius(self.G)
        except nx.NetworkXError:
            return 'inf'

    # centralność wierzchołków (określenie kluczowych użytkowników);
    def calculate_degree_centrality(self):
        return nx.degree_centrality(self.G)

    # gęstość sieci (jak dobrze użytkownicy są “skomunikowani” między sobą); https://networkx.org/documentation/stable/reference/generated/networkx.classes.function.density.html
    def calculate_density(self):
        return nx.density(self.G)

    # średnia długość najkrótszej ścieżki w grafie;
    def calculate_average_shortest_path(self):
        try:
            return nx.average_shortest_path_length(self.G.copy().to_undirected())
        except nx.NetworkXError:
            return nx.NetworkXError
# ewidencja triad - triad census (przy czym ze względu na charakter danych może być to niemożliwe).  https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.triads.triadic_census.html
    def calculate_triadic_census(self):
        return nx.triadic_census(self.G)

    def set_node_data(self, attribute, attribute_name, if_none = 'not_assigned', subattribute = None): ## setuj wlasciwosci wierzcholka
        category_upd_dict = {}
        for node in list(self.G.nodes):
            node_data = json.loads(node)
            node_data_value = node_data[attribute] if subattribute == None else node_data[attribute][subattribute]
            category_upd_dict[node] = node_data_value if node_data_value != None else if_none
        nx.set_node_attributes(self.G, category_upd_dict, name = attribute_name)


#group nodes
    def SNAP_group_nodes(self, attributes):
        groups = nx.snap_aggregation(self.G, node_attributes =  attributes)
        return groups

    def extract_subgraphs(self, attribute, draw = True): ## podziel na podgrafy i zwroc 
        groups = {}
        for (node_name, node_attribute) in self.G.nodes(data = attribute):
            if node_attribute in groups.keys():
                groups[node_attribute].append(node_name)
            else: 
                groups[node_attribute] = []

        subgraphs = {}
        for key in groups.keys():
            #subgraphs[key] = nx.induced_subgraph(self.G, groups[key])
            subgraphs[key] = self.G.subgraph(groups[key])
            if draw:
                self.draw_graph(subgraphs[key], f"{attribute}_{key}.png")
        return subgraphs