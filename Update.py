from ArticleNode import ArticleNode
from PhraseNode import PhraseNode
from KeywordNode import KeywordNode
import psycopg2
import csv


class UpdateKeywords:
    def __init__(self):
        #self.root = root
        print("hi")

    def addKeywords(self, root, wordFile, kDict):
        pid = -1  # article ID starts at 1
        with open(wordFile, 'r', encoding="utf8") as file:
            for line in file:
                pid += 1
                for word in line.split():
                    self.addKeywordToTrie(root, word, pid, kDict)

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
        # Everything finished.  Mark it as the end of a word.
        node.word_finished = True

        #add new KeywordNode to keywordDict
        newKeywordNode = KeywordNode(pid,phrase)
        kDict[pid] = newKeywordNode
    #end addKeywordToTrie

    def getKeywordDict(self, root):
        #root = PhraseNode('*', -1)
        keywordDict = {}

        obj = UpdateKeywords()
        obj.addKeywords(root, "adhoc_wordlist.csv", keywordDict)

        return keywordDict

class UpdateArticles:
    def __init__(self, aDict):
        self.aDict = aDict
        print("")

    def addArticleToDictionary(self, aid, title):
        if aid not in self.aDict:
            newArticle = ArticleNode(aid, title)
            self.aDict[aid] = newArticle

    def addKeywordToDictionary(self, aid, kDict, node):
        currentArticle = self.aDict[aid]
        if node.phraseID not in currentArticle.keywordDict:
            currentArticle.keywordDict[node.phraseID] = node.phrase
            self.aDict[aid] = currentArticle
            keyword = kDict[node.phraseID]
            keyword.referencedByList.append(currentArticle)
            kDict[node.phraseID] = keyword

    def findKeywordInAbstract(self, root, aid, title, abstract, kDict):
        node = root
        #iterate through title
        if title != None:
            for word in title.split():
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
                        self.addArticleToDictionary(aid, title)
                        # Add keywords to current article if it doesn't already exist
                        self.addKeywordToDictionary(aid, kDict, node)
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
        #iterate through abstract
        if abstract != None:
            for word in abstract.split():
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
                        self.addArticleToDictionary(aid, title)
                        # Add keywords to current article if it doesn't already exist
                        self.addKeywordToDictionary(aid, kDict, node)
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
        return self.aDict

    def updateCited(self, aid, title, citedID):
        self.addArticleToDictionary(aid, title)
        self.aDict[aid].cited.append(citedID)
        return self.aDict

    def writeArticleKewords(self, articleDict):
        with open('articleKeywords.csv', mode='w') as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            for aid in articleDict:
                article = articleDict[aid]
                for keyID in article.keywordDict:
                    keyword = article.keywordDict[keyID]
                    id = int(article.articleID)
                    title = str(article.articleTitle)
                    writeArticles.writerow([id,title,keyword])

    def writeArticleCited(self, articleDict):
        with open('articleCited.csv', mode='w') as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            for aid in articleDict:
                article = articleDict[aid]
                for cid in article.cited:
                    id = int(article.articleID)
                    title = str(article.articleTitle)
                    c_id = int(cid)
                    writeArticles.writerow([id,title,cid])
                 
    def writeKeywords(self, keywordDict):
        f = open("keywords.txt", "w+", encoding="utf8")
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
