from ArticleNode import ArticleNode
from DummyNode import DummyNode
import random
from collections import deque
import time

# Test case methods for dummy nodes
def generateDummyNodes(n):
    nodeList = []
    for i in range(1,n+1):
        newNode = ArticleNode(i)
        nodeList.append(newNode)
    return nodeList

def assignDummyKeyWords(nodeList):
    keywordList = ["Facebook","Reddit","Twitter"]
    for node in nodeList:
        numberOfKeywords = random.randint(1,3);
        for i in range(numberOfKeywords):
            node.keywordList.append(random.choice(keywordList))
        node.keywordList= list(set(node.keywordList))

def assignDummyReferences(nodeList):
    for node in nodeList:
        numberOfReferences = random.randint(1,15);
        for i in range(numberOfReferences):
            node.references.append(random.randint(1,100))

def assignDummyAuthors(nodeList):
    authorList = ["Adams", "Jameson", "Smith", "Bernard", "Josiah", "Heaster", "Kadrick", "Fisher", "Cherry", "Howe", "Johns", "Carney", "Rollins", "Meyer", "Garza", "Gonzalez", "Bauer", "Jenkins", "Chase"]		
    for node in nodeList:
        numberOfAuthors = random.randint(1,4);
        for i in range(numberOfAuthors):
            node.authorList.append(random.choice(authorList))
        node.authorList= list(set(node.authorList))
       #print(node.authorList)

def authorSearch(nodeList, authorToSearch):
    articlesByAuthor = []
    for node in nodeList:
        for author in node.authorList: 
            if author == authorToSearch:
                articlesByAuthor.append(node.articleID)
    return(articlesByAuthor)


class multiwayTree:
    def __init__ (self):
        self.root = ArticleNode(0)
        self.Facebook = ArticleNode(-1)
        self.Reddit = ArticleNode(-2)
        self.Twitter = ArticleNode(-3)
        self.nodeDictionary = {
            -3: self.Twitter,
            -2:self.Reddit,
            -1:self.Facebook,
            0:self.root
        }

        self.keywordDictionary = {
            "Twitter" : -3,
            "Reddit"  : -2,
            "Facebook" : -1
        }
        # Initialize root node and its relationships ( this needs to be automated based on keywords)
        self.root.name = "Root"
        self.Facebook.name = "Facebook"
        self.Reddit.name = "Reddit"
        self.Twitter.name = "Twitter"

        self.root.references = [self.Facebook.articleID,self.Reddit.articleID,self.Twitter.articleID]
        self.root.successors = [self.Facebook,self.Reddit,self.Twitter]

        self.Facebook.predecessors = self.root
        self.Reddit.predecessors = self.root
        self.Twitter.predecessors = self.root

        # Tree Variables
        self.numberOfSubtrees= len(self.root.successors)


    def initializeNodeDictionary(self,nodeList):
        for node in nodeList:
            self.nodeDictionary[node.articleID] = node
    
    def assignSubTrees(self):
        for i in range(1,len(self.nodeDictionary)-self.numberOfSubtrees):
            # access node from nodeDictionary
            # Iterate over Keywords
            for keyword in self.nodeDictionary[i].keywordList:
                keywordKey = self.keywordDictionary[keyword]
                self.nodeDictionary[keywordKey].successors.append(self.nodeDictionary[i])
                self.nodeDictionary[i].subTreePredecessors.append(self.nodeDictionary[keywordKey])
    
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
        
    def keyWordSearch(self,keyword):
        
        keyWordPosition = self.keywordDictionary[keyword]
        root  = self.nodeDictionary[keyWordPosition]
        searchOutput = []
        for successor in root.successors:
            searchOutput.append(successor.articleID)
        return searchOutput
            

## Test code 

# Dummy Nodes Test code
startTime = time.time()
nodeList = generateDummyNodes(1000000)
assignDummyKeyWords(nodeList)
assignDummyReferences(nodeList)
assignDummyAuthors(nodeList)
print("Node Generation Time: %s seconds" % (time.time() - startTime))
#MultiwayTree Test code

startTime = time.time()
tree = multiwayTree()
tree.initialize(nodeList)
print("Initializaiton time: %s seconds" % (time.time() - startTime))

startTime = time.time()
searchResults = tree.keyWordSearch("Facebook")
print("Search time: %s seconds" % (time.time() - startTime))

print("Number of Facebook articles: ",len(searchResults))

# Author Dummy Test 
#authorToSearch = "Josiah"
#print("The articles by the author \"", authorToSearch, "\" are: ", authorSearch(nodeList, authorToSearch), "\n")

#print("Authors: ")
#for node in nodeList:
#   print("element ", count, ": ", node.authorList)
#   count+=1


#Tested on dummy nodes only. Change nodeList variable to vary the dummy nodes used

