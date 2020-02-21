from random import randint
from random import randrange
from ArticleNode import ArticleNode
import random
class Tester:
    def __init__ (self,n,keyWordList):
         self.numberOfNodes = n
         self.keywordList = keyWordList
         self.maxReferencesPerNode = 35

    def assignDummyKeyWords(self,node):   
    
        numberOfKeywords = random.randint(1,len(self.keywordList))
        for i in range(numberOfKeywords):
            node.keywordList.append(random.choice(self.keywordList))
        node.keywordList= list(set(node.keywordList))

    def assignDummyReferences(self,node):
        numberOfReferences =  randrange(self.maxReferencesPerNode)
        for i in range(numberOfReferences):
            node.references.append(random.randint(1,self.numberOfNodes))

    def generateDummyNodes(self):
        nodeList = []
        for i in range(1,(self.numberOfNodes+1)):
            newNode = ArticleNode(i,"a")
            nodeList.append(newNode)
            self.assignDummyKeyWords(newNode)
            self.assignDummyReferences(newNode)
        return nodeList

keywordList = ['abc','def']
Test_gen = Tester(10,keywordList)
nodes= Test_gen.generateDummyNodes()
print (len(nodes))