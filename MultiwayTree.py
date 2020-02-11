from ArticleNode import ArticleNode
from DummyNode import DummyNode
import random
from collections import deque
import time
from random import randrange

# Test case methods for dummy nodes
def generateDummyNodes(n):
    nodeList = []
    for i in range(1,n+1):
        newNode = ArticleNode(i)
        nodeList.append(newNode)
    return nodeList

def assignDummyKeyWords(nodeList):
    keywordList = ["Facebook","Reddit","Twitter","Instagram","Snapchat","TikTok"]
    for node in nodeList:
        numberOfKeywords = random.randint(1,len(keywordList))
        for i in range(numberOfKeywords):
            node.keywordList.append(random.choice(keywordList))
        node.keywordList= list(set(node.keywordList))

def assignDummyReferences(nodeList):
    for node in nodeList:
        numberOfReferences =  randrange(30)
        for i in range(numberOfReferences):
            node.references.append(random.randint(1,1000000))


class multiwayTree:
    def __init__ (self):
        self.root = ArticleNode(0)
        self.root.name = "Root"
        self.nodeDictionary = {
            0:self.root
        }
        self.numberOfSubtrees = 0
        self.keywords = []
        
    #Store all the article nodes in node dictionary using Article Id's as keys
    def initializeNodeDictionary(self,nodeList):
        for node in nodeList:
            self.nodeDictionary[node.articleID] = node
            for keyword in node.keywordList:
                if (keyword not in self.keywords):
                    self.numberOfSubtrees = self.numberOfSubtrees + 1
                    self.keywords.append(keyword)
                    self.nodeDictionary[keyword] = ArticleNode(-self.numberOfSubtrees)
                    self.nodeDictionary[keyword].name = keyword
                    self.nodeDictionary[keyword].predecessors = self.root
                    self.root.successors = self.nodeDictionary[keyword]            
    def assignSubTrees(self):
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            for keyword in self.nodeDictionary[i].keywordList:
                self.nodeDictionary[keyword].successors.append(self.nodeDictionary[i])
                self.nodeDictionary[i].subTreePredecessors.append(self.nodeDictionary[keyword]) 
    def establishNodeRelationships(self):
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            for reference in self.nodeDictionary[i].references:
                self.nodeDictionary[i].successors.append(self.nodeDictionary[reference])
                self.nodeDictionary[reference].predecessors.append(self.nodeDictionary[i])
    def initialize(self,nodeList):
        self.initializeNodeDictionary(nodeList)
        self.assignSubTrees()
        self.establishNodeRelationships()
    def printRelations(self):
        print ("Successors: ")
        count = 1
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            print ("element ",count, ": ", end = '')
            count+=1
            for successor in self.nodeDictionary[i].successors:
                print(successor.articleID,end = ' ')
            print()

        count = 1
        print ("\n\nPredecessors:")
        for i in range(1,len(tree.nodeDictionary)-tree.numberOfSubtrees):
            print ("element ",count, ": ", end = '')
            count+=1
            for predecessor in tree.nodeDictionary[i].predecessors:
                print(predecessor.articleID,end = ' ')
            print()   
    def keyWordSearch(self,searchList):
        min = len(self.nodeDictionary)
        searchTree = None

        #find the smallest subTree
        for keyword in searchList:
            if(len(self.nodeDictionary[keyword].successors)<min):
                min = len(self.nodeDictionary[keyword].successors)
                searchTree = self.nodeDictionary[keyword]

        #remove subtree from searchlist
        searchList.remove(searchTree.name)  
        searchOutput = []
        for successor in searchTree.successors:
            if(set(searchList).issubset(set(successor.keywordList))):
                searchOutput.append(successor.articleID)
        return searchOutput
            

## Test code 

# Dummy Nodes Test code
startTime = time.time()
nodeList = generateDummyNodes(1000000)
assignDummyKeyWords(nodeList)
assignDummyReferences(nodeList)
print("Node Generation Time: %s seconds" % (time.time() - startTime))
#MultiwayTree Test code

startTime = time.time()
tree = multiwayTree()
tree.initialize(nodeList)
print("Initializaiton time: %s seconds" % (time.time() - startTime))

startTime = time.time()
searchResults = tree.keyWordSearch(["Facebook","Twitter"])
print("Search time: %s seconds" % (time.time() - startTime))

print("Number of articles :", len(searchResults))
print("Facebook: ",len(tree.nodeDictionary["Facebook"].successors),"Twitter: ",len(tree.nodeDictionary["Twitter"].successors))
#Tested on dummy nodes only. Change nodeList variable to vary the dummy nodes used

