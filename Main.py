from ArticleNode import ArticleNode
from PhraseNode import PhraseNode
from KeywordNode import KeywordNode


class Main:
    def __init__(self):
        print ""

    def addKeywords(self, root, wordFile, kDict):
        pid = -1  # article ID starts at 1
        with open(wordFile, 'r') as file:
            for line in file:
                pid += 1
                for word in line.split():
                    self.addKeywordToTrie(root, word, pid, kDict)

    def addArticleToDictionary(self, aid, aDict):
        global articleDict
        if aid not in aDict:
            newArticle = ArticleNode(aid)
            aDict[aid] = newArticle

    def addKeywordToDictionary(self, aid, aDict, kDict, node):
        global keywordDict
        currentArticle = aDict[aid]
        if node.phraseID not in currentArticle.keywordDict:
            currentArticle.keywordDict[node.phraseID] = node.phrase
            aDict[aid] = currentArticle
            keyword = kDict[node.phraseID]
            keyword.referencedByList.append(currentArticle)
            kDict[node.phraseID] = keyword

    #Trie structure allows for keyword phrases
    def addKeywordToTrie(self, root, phrase, pid, kDict):
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
    def traverseRecords(self, root, text, aDict, kDict):
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
                            # Add article to articleDict if it doesn't already exist
                            self.addArticleToDictionary(aid, aDict)
                            # Add keywords to current article if it doesn't already exist
                            self.addKeywordToDictionary(aid, aDict, kDict, node)
                            #reset node iterator to root
                            node = root
                        continue  # i += 1
                    # if word does not exist in phrase
                    else:
                        if node == root:
                            continue  # i += 1
                        else:
                            node = root
                ### end while
        print ("total # of articles: " + str(aid))
    ### end findPhrases

    def writeArticles(self, articleDict):
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

    def writeKeywords(self, keywordDict):
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
    root = PhraseNode('*', -1)
    # create dictionary of articles (key: articleID, value: ArticleNode)
    articleDict = {}
    # create dictionary of keywords (key: keywordID, value: KeywordNode)
    keywordDict = {}

    obj = Main()
    obj.addKeywords(root, "adhoc_wordlist.csv", keywordDict)
    obj.traverseRecords(root, "sma100.csv", articleDict, keywordDict)
    obj.writeArticles(articleDict)
    obj.writeKeywords(keywordDict)