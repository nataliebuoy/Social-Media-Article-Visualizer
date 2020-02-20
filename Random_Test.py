from ArticleNode import ArticleNode
from GetArticles import GetArticles
from MultiwayTree import multiwayTree
import time
import random
from random import randrange
from random import sample

#Initialize and preprocess data from GetArticles.py
print("Processing Articles:")
generator = GetArticles()
articles = generator.getArticles();
nodeList = list(articles.values())
for node in nodeList:
    node.articleID = int(node.articleID)
    node.references = [int(article) for article in node.cited]
    node.keywordList = list(node.keywordDict.values())

#Initialize DataStructure
tree = multiwayTree()
tree.initialize(nodeList)

#Search parameters

numberOfKeywords = random.randint(1,len(tree.keywords))
numberOfTestSearches = 100
count = 0
successfulSearches=[]
for i in range(numberOfTestSearches):
    searchList = sample(tree.keywords,numberOfKeywords)
    searchResults = tree.keyWordSearch(searchList)
    startTime = time.time()
    tree.keyWordSearch(searchList)
    print("Search time: %s seconds" % (time.time() - startTime))
    print("SearchList: ",searchList)
    print("Search Qualified Articles :", len(searchResults))
    # print("Articles in keywords:-")
    # for keyword in searchList:
    #     print(keyword,": ", len(tree.nodeDictionary[keyword].successors))
    if(len(searchResults)>0) : 
        count+=1
        successfulSearches.append(searchList)
    print()
    print()
print("Successful Searches: ",count,"/",numberOfTestSearches)
categorizedArticles= 0
for keyword in tree.keywords:
    categorizedArticles+=len(tree.nodeDictionary[keyword].successors)

print("Number of Categorized Articles = ",categorizedArticles)
print("All keywords identified: \n", tree.keywords)
print("Successful Searches: \n", successfulSearches)


# import json
# import os
# import glob
# import pprint
# import pandas as pd

# def intersection (list1,list2):
#     return list(set(list1) & set(list2))
# #Convert keywords in adhoc_wordlist.csv into lowercase list of keywords
# keywords= pd.read_csv("adhoc_wordlist.csv")
# df = pd.DataFrame(keywords)
# keywordList = df[["KEYWORDS"]].values.tolist()
# keywordList = [j[0] for j in keywordList]
# keywordList = [x.lower() for x in keywordList]
# keywordList = [x.strip() for x in keywordList]
# print (keywordList)

# # access abstracts of each of the downloaded .json files and check for keywords
# path = '/Users/AgNI/Documents/Capstone/2018-10-25'
# count = 0 
# for filename in glob.glob(os.path.join(path, '*.json')): #only process .JSON files in folder.      
#     with open(filename, encoding='utf-8', mode='r') as currentFile:
#         data=currentFile.read().replace('\n', '')
#         words = json.loads(data)["abstract"]
#         words = words.split()
#         words = [x.strip() for x in words]
#         words = [x.lower() for x in words]
#         words = list(set(words))
#         match = len(intersection(words,keywordList))
#         if match>1 :
#             count+=1
#         #print(list(intersection(words,keywordList)))
# print ("Total Articles hit",count)
