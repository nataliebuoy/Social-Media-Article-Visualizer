from json import JSONEncoder
import random
class edge(JSONEncoder):
    def __init__(self, ident):
        self.id = "n" + str(ident)
        self.source = self.id
        self.target = "n0"