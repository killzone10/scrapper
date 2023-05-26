import urllib.parse
import requests
from helpers import *
import json

''' wiki scraper'''
class WikiError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class WikiScraper:
    def __init__(self, endpoint = 'https://en.wikipedia.org/w/api.php') -> None: 
        self.endpoint = endpoint
    
    def getUrl(self, url, params = {}): ## getUrl zwraca url
        resp = requests.get(url, params=params)
        if not resp.status_code == 200:
            raise WikiError('HTTP ERROR', f"status code: {resp.status_code}")
        print(resp.url)
        return resp.text
    
    #https://en.wikipedia.org/w/api.php?action=opensearch&format=json&search=donald%20trump&formatversion=2
    def query(self, query):
        params = {
            "action": "opensearch",
            "format": "json",
            "formatversion": "2",
            "prop": "description|categories|iwlinks|links|info",
            "search": query
        }
        content = self.getUrl(self.endpoint, params)
        # save_to_file(content, "resp_wiki_query.json")
        
        return json.loads(content)   
    
    
    def search(self, query):
        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srprop": "redirecttitle",
            "srsearch": query
        }
        content = self.getUrl(self.endpoint, params)
        # save_to_file(content, "resp_wiki_search.json")
        
        return json.loads(content)
    
    
    
    #https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donald_Trump&rvslots=*&rvprop=content&format=json
    #   categories:
    # https://commons.wikimedia.org/w/index.php?title=Category:People_by_occupation&from=P
    #
    def scrapPage(self, query):
        params = {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "description|categories|iwlinks|links|info",
            "titles": query
        }
        content = self.getUrl(self.endpoint, params)
        # save_to_file(content, "resp_wiki_scrap.json")

        return json.loads(content)


    #https://en.wikipedia.org/w/api.php?action=query&prop=revisions&titles=Donald_Trump&rvslots=*&rvprop=content&format=json
    #   categories:
    # https://commons.wikimedia.org/w/index.php?title=Category:People_by_occupation&from=P
    #
    def scrapPageId(self, pageid):
        params = {
            "action": "query",
            "format": "json",
            "formatversion": "2",
            "prop": "description|categories|iwlinks|links|info",
            "pageids": pageid
        }
        content = self.getUrl(self.endpoint, params)
        # save_to_file(content, "resp_wiki_scrapid.json")

        return json.loads(content)
    
    
    
    def parseSearchResponse(self, resp):
        try:
            return resp["query"]["search"]
        except KeyError as e:
            print(f'no key: "{e}" in search response')
            return list()        
    
    
    
    def parseSearchResult(self, result):
        try:
            pageid = result["pageid"]
            title = result["title"]
            return pageid, title
        except KeyError as e:
            print(f'no key: "{e}" in search result')
            return None, None
        
        
        
    def matchResult(self, result:dict, user_query:str):
        pageid, title = self.parseSearchResult(result)
        if not (pageid and title): return None
        t_tmp = title.lower().split()
        u_tmp = user_query.lower().split()
        t_tmp.sort()
        u_tmp.sort()
        
        if t_tmp == u_tmp: return pageid
        else: return None
    
    
    
    def matchAllResulsts(self, resp, user_query):
        res:list = self.parseSearchResponse(resp)
        for r in res:
            pageid = self.matchResult(r, user_query)
            if pageid:
                return pageid
        
        return None
    
    
    def parsePageResp(self, page_resp):
        try:
            description = page_resp["query"]["pages"][0]["description"]
            categories = list()
            tmp = page_resp["query"]["pages"][0]["categories"]
            for t in tmp:
                categories.append(t["title"])
            
            return {
                "description": description, 
                "categories": categories
            }
            
        except KeyError as e:
            print(f'no key: "{e}" in page result')
            return None
    
    def scrapWiki(self, user_query):  ## funkcja zwraca czy ktos jest na wikipedii, scrapuje pageid, description i categores
        isOnWiki = False
        res = None
        pageid = None
        try:
            resp = self.search(user_query)
            pageid = self.matchAllResulsts(resp ,user_query)
            print(f"pageid: {pageid}")
            # self.scrapPage("George P. Bush")
            if pageid: ## strona istnieje
                isOnWiki = True
                resp = self.scrapPageId(pageid) ## get id
                res = self.parsePageResp(resp) ## get description i categories
            
        except Exception as e:
            print(f"skip... scrapWiki Exception occured: {e} ")
        
        
        return {
            "is_in_wiki": isOnWiki,
            "wiki_data": res,
            "page_id": pageid
        }
    
    
    
if __name__ == "__main__":
    w = WikiScraper()
    
    r = w.scrapWiki("bush george")
    print(json.dumps(r, indent=2))
    

   