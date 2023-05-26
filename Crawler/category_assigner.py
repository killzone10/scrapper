import json
    #  with open("./dictionary.json", "r", encoding='utf-8') as f:
    # y = json.loads(f.read())

class CategoryAssigner: ## klasa, ktora sluży przypisaniu kategorii !
    def __init__(self):
        self.wiki_data = ""
        self.bio = ""
        self.category_json = open("./dictionary.json", "r", encoding='utf-8') ## słownik dictionary.json który ma słowa kluczowe dla danych kluczy #
        self.category_dict = json.loads(self.category_json.read())
        self.score_dict = {"politics": 0,
                           "politics_engaged": 0,
                           "journalists_writers": 0,
                           "celebrities": 0
                          }
        self.keyword_list = []
        self.category_result = {'b': {'c': None,'k': None}, 
                                "wd": {'c': None,'k': None }, 
                                "wc": {'c': None,'k': None }}
        self.main_category = ""
    
    def set_wiki_data(self, wiki_data): ## wszystkie dane z wikipedii
        self.wiki_data = wiki_data

    def set_bio(self, bio): ## dane z bio parler
        self.bio = bio

    def __reset_score_dict (self): ## zresetowanie dictionary
        self.score_dict = dict.fromkeys(self.score_dict, 0)
    
    def __set_category_result(self, data_source, category): ##setowanie dictionary
        self.category_result[data_source]['c'] = category
        self.category_result[data_source]['k'] = self.keyword_list
        self.__reset_keyword_list()
        self.__reset_score_dict()  

    def __is_in_wiki(self):
        return self.wiki_data['is_in_wiki']

    def __reset_keyword_list(self):
        self.keyword_list = [] 

    def __parse_data(self, data):
        data = data.lower()
        return data
        
    def __parse_data_list(self, data_list):
        return ' '.join(data_list)
        
    #def __update_category_score(self):
        
    ''' funkcja ktora przelicza ile razy wystapilo charakterystyczne slowo wystepujace z danej klasy'''
    def calculate_category_dict(self, data): 
        parsed_data = self.__parse_data(data) 
        for category in self.category_dict:
            for keyword in self.category_dict[category]:
                if keyword in parsed_data:
                    self.keyword_list.append(keyword)
                    self.score_dict[category]+=1

    def find_category(self):
        res = True
        test = list(self.score_dict.values())[0]
        for element in self.score_dict:
            if self.score_dict[element] != test:
                res = False
                break
            
        if res == False:
            max_key = max(self.score_dict, key = self.score_dict.get, default = None) 
            
            return max_key
        return None


    def analise_bio(self): ##analizuj bio##
        try:
            self.calculate_category_dict(self.bio)
            category = self.find_category()
            self.__set_category_result('b', category)
        except Exception as e:
            print(e)
        
    def analise_wiki_dsc(self): ## analizuj description z wiki ##
        try:
            self.calculate_category_dict(self.wiki_data['wiki_data']['description'])
            category = self.find_category()
            self.__set_category_result('wd', category)
        except Exception as e:
            print(e)

    def analise_wiki_categories(self): ## analizuj kategorie z wiki ##
        try:    
            parsed_list = self.__parse_data_list(self.wiki_data['wiki_data']['categories'])
            self.calculate_category_dict(parsed_list)
            category = self.find_category()
            self.__set_category_result('wc', category)

        except Exception as e:
            print(e)
    def assign_main_category(self): ## przypisz głowna kategorie ##
        for data_source in self.category_result:
            category = self.category_result[data_source]['c']
            try:
                self.score_dict[category] += 1
            except KeyError:
                pass
        
        main_category = self.find_category()
        return main_category

    def assign_category(self):
        try:
            self.analise_bio() 
            if self.__is_in_wiki():
                self.analise_wiki_dsc()
                self.analise_wiki_categories()
            # print(self.category_result)
            return self.category_result
        except Exception as e:
            print(e)
 


            

    
    

