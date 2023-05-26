import json
import traceback 
import networkx as nx
from category_assigner import CategoryAssigner
from parler_node import ParlerNode
from Parler import with_auth as authed
from tass_crawler_error import TassCrawlerError
#from graph_utils import *
from helpers import write_raw_json_to_file
# import matplotlib.pyplot as plt
from wiki_scraper import WikiScraper

'''Glowna klasa sluzaca do sciagania danych z parlera'''
class ParlerCrawler:
    def __init__(self, cred_json_file="credentials.json") -> None:
        self.__login: str = None
        self.__passwd: str = None
        self.__auth_session: authed.AuthSession = None ## zalogowanie sie za pomoca credentials.json i utrzymanie sesji

        self.__loadCredentials(cred_json_file) ## load credentials
        self.__auth_session = self.__setupSession() ## ustanow sesje 

        self.__wiki = WikiScraper() ## scraper z wikipedii
        # self.__category = CategoryAssigner()

            
    def __loadCredentials(self, cred_json_file): ## logowanie sie do parlera
        try:
            f = open(cred_json_file, "r", encoding="utf-8")
            tmp = json.loads(f.read())
            self.__login = tmp['login']
            self.__passwd = tmp['password']

        except json.JSONDecodeError as e:
            raise TassCrawlerError('credentials json is not valid json')
        except KeyError as e:
            raise TassCrawlerError(f'invalid credentials json key: {e}')
        except FileNotFoundError as e:
                raise TassCrawlerError(f'credentials json file not found: {cred_json_file}')



    def __setupSession(self): ## utrzymanie sesji 
        try:
            au = authed.AuthSession(debug=False)
            au.login(
                identifier= self.__login,
                password= self.__passwd
            )
            if(not au.is_logged_in):
                raise TassCrawlerError("authorization failed")
        except Exception as e:
            raise TassCrawlerError(f"Login exception: {e}")

        return au



####################################################################################################
#------------------ APi maethods
####################################################################################################


    def getUserFollowing(self, userName): ### pobieranie danych uzytkownika
        ret = self.__auth_session.following(userName)

        return ret


    def getUserStats(self, username:str):
        ret = self.__auth_session.profile(username)
        return ret


    def getUserFollowingList(self, root_username: str= ""): 
        tmp:dict = self.getUserFollowing(root_username)
        if not "data" in tmp: 
            raise TassCrawlerError('no "data" key in following response')

        return tmp['data']


####################################################################################################
#------------------- build graph methods 
####################################################################################################

    def __parseNode(self, status_resp:dict): ## ustaw w nodzie dane - zapdatuj noda
        try:
            d = status_resp["data"]
            follower_cnt = d["follower_count"] 
            follwing_cnt = d["following_count"] 
            name = d["name"] 
            username = d["username"] 
            uuid = d["uuid"] 
            bio = d["bio"] 
            
            return ParlerNode(follower_cnt, follwing_cnt, name, username, uuid, bio)
        except KeyError as e:
            raise TassCrawlerError(f'no "{e}" key in following response')


    ''' funkcja ponizej zwraca w tmp inofmrację pobrane z parlera, następnie przypisuje je do noda, potem sciąga dane z wiki i aktualizuje "category"'''

    def __scrapNode(self, username): ## 
        try:
            tmp = self.getUserStats(username) ## scrap z parlera
            node = self.__parseNode(tmp) ## przypisanie do node
            self.__category = CategoryAssigner()
            self.__updateWithWikiInfo(node) ## scrap i update o wiki info
            self.__updateCategory(node)
        
            return node
        except TassCrawlerError as e:
            raise e
        


    def __updateWithWikiInfo(self, node:ParlerNode):
        d = self.__wiki.scrapWiki(node.name) ## scra z wiki
        node.setWikiData(d) ## update node o wiki info

    def __updateCategory(self, node:ParlerNode): ## update o kategorie (bio, desc i cat)
        self.__category.set_wiki_data(node.wiki_data)
        self.__category.set_bio(node.bio)

        category = self.__category.assign_category()
        main_category = self.__category.assign_main_category()

        node.setCategory(category)
        # node.setCategory(category.copy())
        node.setMainCategory(main_category)

    def __buildNode(self, user_obj):
        if not("username" in user_obj and "name" in user_obj):
            raise TassCrawlerError('no "username" or "name" key in __buildNode user_obj')

        return self.__scrapNode(user_obj["username"])


    def __processChildUser(self, root_node, child_user, depth, G): ## rekurencyjne szukanie w głąb razem z buildgraph
        try:
            child_node = self.__buildNode(child_user) ## build node
            G.add_edge(root_node, child_node) ## dodanie krawedzi
            self.__buildGraph(child_node, child_node.username, depth, G) ## child moze byc parentem, więc odpala buildd graphu
        except TassCrawlerError as e:
            print(f"ERROR: {e}")
        except Exception as e:
            traceback.print_stack()
            print(f"ERROR: {e}")
            


    def __buildGraph(self, root_node, root_username:str, depth:int, G: nx.DiGraph) -> nx.DiGraph: ## dla okreslonej glebokosci analizujemy root nazwisko
        if depth < 1: return # zmniejszamy glebokosc o 1
        depth-=1       
        
        try:
            foolowing = self.getUserFollowingList(root_username) ## dla root usera bierzemy following liste i dla nich odpalamy
            for child_user in foolowing:
                self.__processChildUser(root_node, child_user, depth, G) ## rekurencyjnie process child user

        except TassCrawlerError as e:
            traceback.print_stack()
            print(f"ERROR: {e}")
            input("Exception, press key to continue")



    def getFollowingGraph(self, root_username: str= "", depth: int = 2) -> nx.DiGraph:
        G = nx.DiGraph()
        root_node = self.__scrapNode(root_username)
        G.add_node(root_node)
        self.__buildGraph(root_node, root_username, depth, G)

        return G
