# import matplotlib.pyplot as plt

from parler_crawler import ParlerCrawler, TassCrawlerError, ParlerNode
from graph_utils import *
import os


def addUserToGraph(G, c, username, depth=2): ## funkcje dzieki ktorym mozna dodać do obecnego grafu uzytkownikow
	H:nx.DiGraph = c.getFollowingGraph(root_username= username, depth = depth)
	combineGraphs(G, H)

''' ## storzenie glownego obiektu Crawlera - podanie listy uzytkownikow, ktorzy maja byc scrapowani i glebokosci do jakiej ma być wykonywane scrapowanie'''
def getParlerGraph(G, users_list,depth=2):
	c = ParlerCrawler()
	for username in users_list:
		addUserToGraph(G, c, username=username, depth=depth)


if __name__ == "__main__":
	pass
	# try:
		
		# add = 0
		# if (add == 0):
		# 	fp = open('t.edgelist','w')
		# 	fp.close()
			
		# G = read_graph(filename="t.edgelist")
		# users_list = ["ConceptualJames"]
		# users_list = ["TedCruz", "RepMattGaetz","RogerStone"]  ## republikanie ##RogerStone to doradca poityczny
		# users_list = ['DineshDSouza','Kirstiealley','TitoOrtiz'] ## tworcy\celebrities 
		# users_list = ['TuckerCarlson', 'Cassandra MacDonald','AndrewWilkow','Mariabartiromotv','SeanHannity','Marklevinshow'] ##dziennikarze
		# users_list = ["TedCruz"]
		#users_list = ["Jsayang"]

		# filepath = '../edgelists/'
		# filename = 'politicians_matches.txt'
		# with open(f"{filepath}{filename}")as f:
		# 	all_users = f.read().split(',')
		# i = 40
		# step = 20
		# while i < len(all_users):
		# 	users_list = all_users[i: i + step] if i + step < len(all_users) - 1 else all_users[i:]
		# 	i+=step
		# 	G = nx.DiGraph() 
		# 	edgelist_filename = f"{filename[:-4]}_{i}.edgelist"
		# 	print(edgelist_filename)
		# 	getParlerGraph(G,users_list, depth=1)
		# 	save_graph(G, filename=edgelist_filename)

	# except TassCrawlerError as e:
	# 	print(f"[Error] {e}")


