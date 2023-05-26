from networkx.utils.decorators import open_file

@open_file(1, mode="wb")
def write_edgelist(G, path, comments="#", delimiter=" ", data=True, encoding="utf-8"): ## pisz do edgelist


    for line in generate_edgelist(G, delimiter, data):
        line += "\n"
        path.write(line.encode(encoding))
        

def generate_edgelist(G, delimiter=" ", data=True): ## generuj edgelist
    if data is True:
        for u, v, d in G.edges(data=True):
            e = u, v, dict(d)
            yield delimiter.join(map(repr, e))
    elif data is False:
        for u, v in G.edges(data=False):
            e = u, v
            yield delimiter.join(map(repr, e))
    else:
        for u, v, d in G.edges(data=True):
            e = [u, v]
            try:
                e.extend(d[k] for k in data)
            except KeyError:
                pass  # missing data for this edge, should warn?
            yield delimiter.join(map(str, e))