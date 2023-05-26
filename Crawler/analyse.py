import networkx as nx
from random import sample
from math import pow
import numpy as np
import json 
import matplotlib.pyplot as plt
from graph_utils import read_graph, combineGraphs, save_graph
from graph_analiser import GraphAnaliser
import pandas as pd
from IPython.display import display

###
# rozkład stopni wierzchołków, 
''' funkcja odpowiedzialna za przeanalzowanie grafu i jeśli to możliwe rozdzielenia grafu na podgrafy po main category i is in wiki
zwraca graf pogrupowany po main category, graf z is_in_wiki, największą składow spójną oraz wyniki z analizy grafu'''

def do_all_analysis(graph, graph_name, directed = True, type = "entire_graph"): 
    result = {'graph_type':f'{type}'} ### wyjsciowe dictionary
    ga = GraphAnaliser(graph, graph_name = graph_name) ## klasa, w której analizowany jest graf
    nodes, edges = ga.print_graph_info()
    result['nodes'] = nodes 
    result['edges'] = edges ## dodaj nody i edge do result

    ga.set_node_data(attribute='main_category', attribute_name='main_category')
    ga.set_node_data(attribute='wiki_data', attribute_name='is_in_wiki', subattribute='is_in_wiki')

    sub_main = ga.extract_subgraphs('main_category') ## ekstrakcja grafu po main_category
    sub_wiki = ga.extract_subgraphs('is_in_wiki') ## ekstrakcja grafu po is_in wiki
    
    degrees = ga.calculate_degrees()
    print(f"degrees: {degrees}")
    mean_degree = ga.calculate_mean_degree(degrees)
    print(f"mean degree: {mean_degree}")
    result['mean_degree'] = mean_degree
    
    ga.plot_degree_distribution(degrees, name = 'degree_dst_graph.png') ## wyplotowanie dystrybucj stopni
    
    diameter = ga.calculate_diameter()
    print(f"diameter: {diameter}")
    result['diameter'] = diameter

    radius = ga.calculate_radius()
    print(f"radius: {radius}")
    result['radius'] = radius

    degree_centrality = ga.calculate_degree_centrality()
    # print(f"degree centrality {degree_centrality}")

    density = ga.calculate_density()
    print(f"density: {density}")
    result['density'] = density

    average_shortest_path = ga.calculate_average_shortest_path()
    print(f"avg shortest path: {average_shortest_path}")
    result['average_shortest_path'] = average_shortest_path

    if directed:
        triadic_census = ga.calculate_triadic_census()
        print(f'triadic census: {triadic_census}')
        result['triadic_census'] = triadic_census ## jesli graf jest skierowany policz triady

    bcc = ga.biggest_connected_component()
    return sub_main, sub_wiki, bcc, result ## return
    
''' funkcja służąca stworzeniu wykresu slupkowego, który przedstawia kategorie od ilości użytkownikow'''
def create_histogram(hist_data, name):
    plt.clf()
    plt.bar(hist_data.keys(), hist_data.values())
    y_pos = range(len(hist_data.keys()))
    plt.xticks(y_pos, hist_data.keys(), rotation = 90)
    plt.tight_layout()
    plt.savefig(f"amountof_group_type_{name}")

def main():
    print('\nLOADING DATASETS ')
    group = 'all_data'
    # group = 'journalists'
    type = 'seed'
    type = 'connected' 
    results = pd.DataFrame(columns = ['graph_type', 'nodes', 'edges', 'mean_degree', 'diameter', 'radius', 'density', 'average_shortest_path','triadic_census']) ## init koncowej tabelki z wynikami zapisywanej jako out.csv
    filename = f"{group}_{type}.edgelist" ## init nazwy pliku ##
    graph = read_graph(filepath = "datasets/", filename = filename) ## wczytanie grafu
    graph.remove_edges_from(nx.selfloop_edges(graph)) ## usuniecie duplikatów
    hist_data = {}
    print('-------------analising graph----------------')
    sub_main, sub_wiki, bcc, result = do_all_analysis(graph, graph_name = f"{group}_{type}") ### wrzucamy do analizy cały graf
    results = results.append(result, ignore_index = True)  
    print('subgraphs_main_category') 
    for cat in sub_main.keys(): ## sprawdzamy kategorie jakie zostały zwrócone po main_category wraz  z licznością
        print(f'Category {cat}')
        print(f"count {sub_main[cat].number_of_nodes()}")
        hist_data[cat] = sub_main[cat].number_of_nodes()
    create_histogram(hist_data, "sub_main") ## plotujemy##
        ## tutaj histogram dla calego zbioru

    print('-------------analising wiki data------------') 
    wiki_graph = sub_wiki[True]
    sub_main_wiki, _, _, wiki_result = do_all_analysis(wiki_graph, graph_name = f"{group}_{type}_in_wiki", type = 'wiki_graph') ## powtarzamy to dla grafu, którego wierzcholki są w wikipedii !
    results = results.append(wiki_result, ignore_index = True)  

    for cat in sub_main_wiki.keys():
        print(f'Category {cat}')
        print(f"count {sub_main_wiki[cat].number_of_nodes()}")
        hist_data[cat] = sub_main_wiki[cat].number_of_nodes()
        ## histogram
    create_histogram(hist_data, "sub_main_wiki") ## ponowny wykres slupkowy - tym razem dla wiki #

    ##agregacja##
    print('-------------analising biggest connected component ----------------')
    _,_,_, bcc_result = do_all_analysis(bcc, 'bcc', directed = False, type = "bcc") ## analiza największej składowej spójnej##
    results = results.append(bcc_result, ignore_index = True)  

    ## analiza  subgrafów z wiki po main_category, ekstrakcja grup i analiza samych tych grup ##
    for cat in sub_main_wiki.keys():
        _, _, _, result = do_all_analysis(sub_main_wiki[cat], 'is_in_wiki' + cat, directed = True, type = 'is_in_wiki' + cat) 
        results = results.append(result, ignore_index = True)  

    results.to_csv("out.csv") ## rezultaty do csv
    display(results)

    
    
if __name__ == "__main__":
    main()
    