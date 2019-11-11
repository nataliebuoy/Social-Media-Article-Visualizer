from ArticleNode import ArticleNode
from PhraseNode import PhraseNode
from KeywordNode import KeywordNode


class Main:
    #create dictionary of articles (key: articleID, value: ArticleNode)
    articleDict = {}
    #create dictionary of keywords (key: keywordID, value: KeywordNode)
    keywordDict = {}

    root = PhraseNode('*', -1)

    def addArticleToDictionary(self, aid, aDict):
        global articleDict
        # add articleID to dictionary if it doesn't already exist
        if aid not in aDict:
            newArticle = ArticleNode(aid)
            aDict[aid] = newArticle


    #Trie structure allows for keyword phrases
    def addKeywordToTrie(root, phrase, pid, kDict):
        global keywordDict

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

        #add new KeywordNode to keywordDict
        newKeywordNode = KeywordNode(pid,phrase)
        kDict[pid] = newKeywordNode
    #end addKeywordToTrie

    # https://www.toptal.com/algorithms/needle-in-a-haystack-a-nifty-large-scale-text-search-algorithm
    def traverseRecords(root, text, aDict, kDict):
        global articleDict
        global keywordDict

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
                    # check if word exists in phrase
                    for child in node.children:
                        childIndex += 1
                        if word == child.phrase:
                            flag = True
                            break
                    #if word exists in phrase:
                    if flag:
                        node = node.children[childIndex]
                        if node.word_finished:

                            #addArticleToDictionary(aid, aDict)

                            # Add article to articleDict if it doesn't already exist
                            if aid not in aDict:
                                newArticle = ArticleNode(aid)
                                aDict[aid] = newArticle

                            # Add keywords to current article if it doesn't already exist
                            currentArticle = aDict[aid]
                            if node.phraseID not in currentArticle.keywordDict:
                                currentArticle.keywordDict[node.phraseID] = node.phrase
                                aDict[aid] = currentArticle

                                keyword = kDict[node.phraseID]
                                keyword.referencedByList.append(currentArticle)
                                kDict[node.phraseID] = keyword

                            #reset node iterator to root
                            node = root

                        continue  # i += 1
                    # if word does not exist in phrase
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
        f.write("'articleID','keyword'\n")

        for aid in articleDict:
            keys = ""
            article = articleDict[aid]
            for keyID in article.keywordDict:
                keyword = article.keywordDict[keyID]
                keys += str(keyword) + ","
            f.write("'%d','%s'\n" % (aid,keys))
        f.close()
    #end writeArticles

    def writeKeywords(keywordDict):
        f = open("keywords.txt", "w+")
        f.write(str(len(keywordDict)) + "\n")  # total number of keywords
        f.write("'articleCount','keyword','articleID'\n")

        for keyID in keywordDict:
            keywordNode = keywordDict[keyID]
            articles = ""
            count = len(keywordNode.referencedByList)
            for articleNode in keywordNode.referencedByList:
                articles += str(articleNode.articleID) + ","
            f.write("'%d','%s','%s'\n" % (count, keywordNode.keyword, articles))
        f.close()
    # end writeKeywords

    if __name__ == "__main__":
        addKeywordToTrie(root, "Facebook", 0, keywordDict)
        addKeywordToTrie(root, "Twitter", 1, keywordDict)
        addKeywordToTrie(root, "Reddit", 2, keywordDict)
        addKeywordToTrie(root, "Instagram", 3, keywordDict)
        addKeywordToTrie(root, "LinkedIn", 4, keywordDict)
        addKeywordToTrie(root, "chemoradiation", 5, keywordDict)
        addKeywordToTrie(root, "content", 6, keywordDict)
        addKeywordToTrie(root, "marketing", 7, keywordDict)
        addKeywordToTrie(root, "normalization", 8, keywordDict)
        addKeywordToTrie(root, "knowledge", 9, keywordDict)
        addKeywordToTrie(root, "research", 10, keywordDict)

        traverseRecords(root, "sma", articleDict, keywordDict)
        writeArticles(articleDict)
        writeKeywords(keywordDict)
