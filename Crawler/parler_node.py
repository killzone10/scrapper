from dataclasses import dataclass, asdict
from dacite import from_dict
from json import loads as json_loads
from json import dumps as json_dumps
#{'bio': {'category': None,'keywords': None }, "wiki description": {'c': None,'k': None }, "wiki categories": {'c': None,'k': None }
@dataclass
class ParlerNode: ## glowny parler node
	follower_cnt: int ## followersi
	follwing_cnt: int ## followani
	name:str ## nazwa
	username: str ## nzwa uzytkowika
	uuid: str # numer id
	bio: str = "" # bio
	wiki_data: dict = None
	category: dict = None 
	main_category: str = '' ## kategoria glowna noda

	
	''' funckje ponizej to standardowe settery i gettery'''
	def __eq__(self, other):
		return self.username == other.username

	def __hash__(self):
		return hash(self.username)

	def __str__(self) -> str:
		return self.username

	def __repr__(self) -> str:
		tmp = json_dumps(asdict(self))
		return tmp
	
	def getWikiData(self):
		return self.wiki_data

	def setWikiData(self, data):
		self.wiki_data = data

	def setCategory(self, category):
		self.category = category
	
	def setMainCategory(self, category):
		self.main_category = category
 
	@staticmethod 
	def parse(node_str:str): ## parsuj 
		node = from_dict(data_class=ParlerNode, data=json_loads(node_str))
		return node
