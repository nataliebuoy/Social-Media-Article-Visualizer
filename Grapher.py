import random
import time
import json
import os
import glob
import pandas as pd
from random import sample
from random import randrange
from ArticleNode import ArticleNode
from GetArticles import GetArticles
from MultiwayTree import multiwayTree
from RunDatabase import RunDB
from node import node, nodeEncoder
from edge import edge

class grapher:

    def generateKeywordGraph(self, searchResult, kw):
        art = ArticleNode()
        dummyThiccGraph = {'nodes': [], 'edges': []}
        nodeList = []
        edgelist = []
        xie = 0
        yie = 0
        #print("graphGenerator: " + str(searchResult))
        for x in searchResult:
            xie += 1
            yie += 1
            randColor = "#{:06x}".format(random.randint(0, 0xFFFFFF))
            testNode = node(str(x),str(x),2,random.randint(-100,100),random.randint(-100,100), randColor)
            nodeList.append(testNode)
            for z in searchResult[x]:
                if(x == "Undefined"):
                    articleNode = node(str(z),str(z), 1,random.randint(-100,100),random.randint(-100,100), randColor)
                    nodeList.append(articleNode)
                    articleEdge = edge(str(z), str(x))
                    edgelist.append(articleEdge)
                    print("Category: " + str(x) + " article: " + str(z))

                else:
                    label = "Title: " + str(z.getTitle()) + " ArticleID: " + str(z.getInfo()) + " SubCategory: " + str(z.getSubCat())
                    articleNode = node(str(z.getInfo()),label, 1,random.randint(-100,100),random.randint(-100,100), randColor)
                    nodeList.append(articleNode)
                    articleEdge = edge(str(z.getInfo()), str(x))
                    edgelist.append(articleEdge)
                    print("Category: " + str(x) + " article: " + str(z.getInfo()))
        randColor0 = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        nodObj = node(kw, kw,3,0,0, randColor0)
        nodeList.insert(0,nodObj)
        for x in searchResult:
            testEdge = edge(str(x), kw)
            edgelist.append(testEdge)

        dummyThiccGraph['nodes'] = [node.__dict__ for node in nodeList]
        dummyThiccGraph['edges'] = [edge.__dict__ for edge in edgelist]
        output = dummyThiccGraph
        print(dummyThiccGraph['nodes'])
        with open(os.path.join('static', 'testjson.json'), 'w') as outfile:
            outfile.write(json.dumps(output, indent=4))
        return output

    def generateAuthorGraph(self, authorlist):
        print("authorGraph Method")
        for x in authorlist:
            print(x)

        return authorlist