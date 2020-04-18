from json import JSONEncoder
import random
class node(JSONEncoder):
    def __init__(self, ident, name, nodeSize):
        self.id = "n" + str(ident)
        self.label = name
        self.x = random.randint(-10000, 10000)
        self.y = random.randint(-10000, 10000)
        self.size = nodeSize
        self.color = "#FFFF00"

class nodeEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

def obj_dict(node):
    return node.__dict__
