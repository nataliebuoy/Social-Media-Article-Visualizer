from ArticleNode import ArticleNode
from GetArticles import GetArticles
from MultiwayTree import multiwayTree
from random import randrange

generator = GetArticles()
articles = generator.getArticles();
nodeList = list(articles.values())

tree = multiwayTree()
tree.initialize(nodeList)
print(tree.nodeDictionary[randrange(10000)].successors)