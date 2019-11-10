from ArticleNode import ArticleNode
from PhraseNode import PhraseNode

class Main:
    #create dictionary of articles (key: articleID, value: ArticleNode)
    articleDict = {}

    root = PhraseNode('*', -1)

    def addArticle(articleID, aList):
        # add articleID to list if it doesn't already exist
        if articleID not in aList:
            article = ArticleNode(articleID)

    def addPhrase(root, phrase, pid):
        word = []
        word = phrase.split()
        node = root
        i = 0
        while i < len(word):
            found_in_child = False
            for child in node.children:
                if child.phrase == word[i]:
                    child.counter += 1
                    node = child
                    found_in_child = True
                    break
            # We did not find it so add a new child
            if not found_in_child:
                new_node = PhraseNode(word[i], pid)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
            if i == len(word) - 1:
                node.phraseID = pid
            i += 1
        # Everything finished. Mark it as the end of a word.
        node.word_finished = True

    # https://www.toptal.com/algorithms/needle-in-a-haystack-a-nifty-large-scale-text-search-algorithm
    def findPhrases(root, text, aDict):
        global articleDict

        node = root

        # Traverses file without saving items to memory
        aid = -1    # article ID starts at 1
        with open(text, 'r') as file:
            for line in file:
                aid += 1
                print "article: " + str(aid)
                for word in line.split():
                    flag = False
                    childIndex = -1
                    #find if word exists in PhraseList
                    for child in node.children:
                        childIndex += 1
                        if word == child.phrase:
                            flag = True
                            break
                    #if word exists in PhraseList:
                    if flag:
                        node = node.children[childIndex]
                        if node.word_finished:

                            # Add article to articleDict if it doesn't already exist
                            if aid not in aDict:
                                newArticle = ArticleNode(aid)
                                aDict[aid] = newArticle

                            # Add keywords to current article if it doesn't already exist
                            currentArticle = aDict[aid]
                            if node.phraseID not in currentArticle.keywordDict:
                                currentArticle.keywordDict[node.phraseID] = node.phrase
                                aDict[aid] = currentArticle

                            #reset node iterator to root
                            node = root

                        continue  # i += 1
                    else:
                        if node == root:
                            continue  # i += 1
                        else:
                            node = root
                        ###
                    ###
                ### end while
        print ("total # of articles: " + str(aid))
    ### end findPhrases

    def writeArticles(articleDict):
        f = open("articles.txt", "w+")
        f.write(str(len(articleDict)) + "\n") # total number of articles
        f.write("'articleID','keywordID'\n")
        print("------------------------")
        #print("count: " + str(len(articleDict)))
        #print("'articleID','keywordID'")

        for aid in articleDict:
            keys = ""
            article = articleDict[aid]
            for keyID in article.keywordDict:
                keyword = article.keywordDict[keyID]
                keys += str(keyword) + ","
            f.write("'%d','%s'\n" % (aid,keys))
            #print("'%d','%s'" % (aid, keys))
        f.close()
    #end writeArticles

    addPhrase(root, "Facebook", 0)
    addPhrase(root, "Twitter", 1)
    addPhrase(root, "Reddit", 2)
    addPhrase(root, "innovative", 3)
    addPhrase(root, "chemoradiation", 4)
    addPhrase(root, "importance", 5)
    addPhrase(root, "content", 6)
    addPhrase(root, "marketing", 7)
    addPhrase(root, "normalization", 8)
    addPhrase(root, "knowledge", 9)
    addPhrase(root, "research", 10)

    findPhrases(root, "sma", articleDict)
    writeArticles(articleDict)