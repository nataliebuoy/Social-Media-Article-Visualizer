from ArticleNode import ArticleNode
from PhraseNode import PhraseNode


class Main:
    articleList = []
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
    def findPhrases(root, text, aList):
        global articleArray

        node = root
        foundPhrases = []

        # Traverses file without saving items to memory
        aid = -1    # article ID starts at 1
        with open(text, 'r') as file:
            for line in file:
                aid += 1
                print "article: " + str(aid)
                for word in line.split():
                    flag = False
                    childIndex = -1
                    for child in node.children:
                        childIndex += 1
                        if word == child.phrase:
                            flag = True
                            break
                    if flag:
                        node = node.children[childIndex]
                        if node.word_finished:
                            foundPhrases.append(node.phraseID)

                            #create an article node

                            # add articleID to list if it doesn't already exist

                            articleFound = False
                            articleIndex = 0
                            while articleIndex < len(aList):
                                if aid == aList[articleIndex].articleID:
                                    articleFound = True
                                    break
                                articleIndex += 1
                            if articleFound == False:
                                article = ArticleNode(aid)
                                aList.append(article)

                            # add keyword phrase to current article
                            # find article
                            articleIndex = 0

                            keyFound = False
                            keyIndex = 0
                            while keyIndex < len(article.keywords):
                                if node.phraseID == article.keywords[keyIndex]:
                                    keyFound = True
                                    break
                                keyIndex += 1
                                #print "keyword loop"
                            if keyFound == False:
                                article.keywords.append(node.phraseID)

                            #reset node iterator to root
                            node = root
                        continue  # i += 1
                    else:
                        if node == root:
                            continue  # i += 1
                        else:
                            node = root
                            # else statement should remain on the same word instead of iterating - not sure?
                        ###
                    ###
                ### end while
                #if node.phraseID != -1:
                #    foundPhrases.append(node.phraseID)
        #print foundPhrases
    ### end findPhrases

    def write(articleList):
        f = open("articles.txt", "w+")
        f.write("'articleID','keywordID'\n")
        print("------------------------")
        print("'articleID','keywordID'")
        for article in articleList:
            keys = ""
            for keyword in article.keywords:
                keys += str(keyword) + " "
            f.write("'%d','%s'\n" % (article.articleID,keys))
            print("'%d','%s'" % (article.articleID, keys))
        f.close()
    #end write

    addPhrase(root, "Facebook", 0)
    addPhrase(root, "Twitter", 1)
    addPhrase(root, "Reddit", 2)
    addPhrase(root, "innovative", 3)
    addPhrase(root, "sectorial", 4)
    addPhrase(root, "importance", 5)
    addPhrase(root, "content", 6)
    addPhrase(root, "marketing", 7)
    addPhrase(root, "Provincial", 8)
    addPhrase(root, "knowledge", 9)
    addPhrase(root, "research", 10)

    findPhrases(root, "sma100.csv", articleList)
    write(articleList)