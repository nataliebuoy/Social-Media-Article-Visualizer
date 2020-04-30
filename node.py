from json import JSONEncoder
import random
class node(JSONEncoder):
    def __init__(self, ident,label, nodeSize, x, y, color):
        self.id = str(ident)
        self.label = label
        self.x = x
        self.y = y
        self.size = nodeSize
        self.color = color
        self.count = nodeSize

class nodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def obj_dict(node):
    return node.__dict__
