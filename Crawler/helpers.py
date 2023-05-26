from json import dumps
import re
def save_to_file(data, file): ## zapisz do pliku
    with open(file, "w", encoding='utf-8') as f:
        f.write(data)

def write_raw_json_to_file(content, file = "tmp.json"): ## zapisz do json
    save_to_file(dumps(content), file)
    

def extract_usernames_edgelist(filepath = "./", filename = "graph.edgelist"): ## exractuj z usernames edgelist
    usernames = set()
    with open(f"{filepath}{filename}") as f:
        file = f.read()
    matches = re.findall(r'(?<=\"username":)(.*?)(?=\,)', file)
    matches = [m[2:-1] for m in matches]
    return ','.join(set(matches))

    

# matches = extract_usernames_edgelist(filepath = 'edgelists/',filename = "t.edgelist")
# save_to_file(matches, file = 'politicians_matches.txt')
