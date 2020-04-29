from json import JSONEncoder
import random
class node(JSONEncoder):
    def __init__(self, ident, nodeSize):
        self.id = str(ident)
        self.label = ident
        self.x = random.randint(-10, 10)
        self.y = random.randint(-10, 10)
        self.size = nodeSize
        self.color = "#FFFF00"
        self.count = nodeSize

class nodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def obj_dict(node):
    return node.__dict__
