from json import JSONEncoder
import random
class edge(JSONEncoder):
    def __init__(self, ident, kw):
        self.id = str(ident)
        self.source = ident
        self.target = kw
        self.type = "arrow"