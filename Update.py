from ArticleNode import ArticleNode
from PhraseNode import PhraseNode
from KeywordNode import KeywordNode
import psycopg2
import csv


class UpdateKeywords:
    def __init__(self):
        print("Updating")

    def addKeywords(self, root, wordFile, kDict):
        counter = 0
        pid = -1  # article ID starts at 1
        with open(wordFile, 'r', encoding="utf8") as file:
            for line in file:
                if counter != 0:
                    self.addKeywordToTrie(root, line, pid, kDict)
                counter += 1
                pid += 1

                #pid += 1
                #for word in line.split():
                    #if counter != 0:
                        #self.addKeywordToTrie(root, word, pid, kDict)
                    #counter += 1

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
                new_node = PhraseNode(word[i].lower().strip(), pid)
                node.children.append(new_node)
                # And then point node to the new child
                node = new_node
            if i == len(word) - 1:
                node.phraseID = pid
            i += 1
        # Everything finished.  Mark it as the end of a word.
        node.word_finished = True

        #add new KeywordNode to keywordDict
        newKeywordNode = KeywordNode(pid,phrase.lower().strip())
        kDict[pid] = newKeywordNode
    #end addKeywordToTrie

    def getKeywordDict(self, root):
        keywordDict = {}

        obj = UpdateKeywords()
        obj.addKeywords(root, "adhoc_wordlist.csv", keywordDict)

        return keywordDict

class UpdateArticles:
    def __init__(self, aDict):
        self.aDict = aDict
        print("")

    #function to create article with id and title
    def addArticleToDictionary(self, aid, title, contains_social_media):
        if aid not in self.aDict:
            newArticle = ArticleNode(int(aid), title)
            newArticle.contains_social_media = contains_social_media
            self.aDict[aid] = newArticle
        return self.aDict

    #function to update cited
    def updateCited(self, aid, title, citedID):
        self.aDict = self.addArticleToDictionary(citedID, title, False)
        self.aDict[aid].cited.append(citedID)
        self.aDict[aid].references.append(int(citedID))
        return self.aDict

    def updateCitedBy(self, aid, title, citedByID):
        self.aDict = self.addArticleToDictionary(citedByID, title, False)
        self.aDict[aid].citedBy.append(citedByID)
        return self.aDict

    def updateAuthor(self, aid, author_name):
        if aid in self.aDict:
            self.aDict[aid].authorList.append(author_name)
        return self.aDict

    def updateJournal(self, aid, journal_name, subject_area, subject_category):
        if aid in self.aDict:
            self.aDict[aid].journal = journal_name
            self.aDict[aid].subject_area = subject_area
            self.aDict[aid].subject_category = subject_category
        return self.aDict

    #------------------------KEYWORD-RELATED FUNCTIONS------------------------

    #function to update keyword list and add to article
    def addKeywordToDictionary(self, aid, kDict, node, key):
        currentArticle = self.aDict[aid]
        if node.phraseID not in currentArticle.keywordDict:
            currentArticle.keywordDict[node.phraseID] = key
            self.aDict[aid] = currentArticle
            keyword = kDict[node.phraseID]
            keyword.referencedByList.append(currentArticle)
            kDict[node.phraseID] = keyword
            currentArticle.keywordList.append(key)

    #function parses through abstract/title of every article and stores found keywords in respective article node
    def findKeywordInArticle(self, root, aid, title, abstract, kDict):
        node = root
        key = ""

        containsSocialMedia = False

        #iterate through title
        if title != None:
            for word in title.split():
                word = word.lower().strip()

                if word == "social" or word == "media" or word == "socialmedia" or word == "social-media" or word == "social media":
                    containsSocialMedia = True

                flag = False
                childIndex = -1
                # check if word exists in phrase
                for child in node.children:
                    childIndex += 1
                    if word.lower() == child.phrase.lower():
                        flag = True
                        break
                #if word exists in phrase:
                if flag:
                    key += word
                    node = node.children[childIndex]
                    if node.word_finished:
                        self.addKeywordToDictionary(aid, kDict, node, key)
                        key = ""
                        node = root
                    else:
                        key += " "
                    continue
                # if word does not exist in phrase
                else:
                    if node == root:
                        key = ""
                        continue  # i += 1
                    else:
                        node = root
                        key = ""
                        
                        #CASE B
                        flag2 = False
                        childIndex = -1
                        for child in node.children:
                            childIndex += 1
                            if word.lower() == child.phrase.lower():
                                flag2 = True
                                break
                        #if word exists in phrase:
                        if flag2:
                            key += word
                            node = node.children[childIndex]
                            if node.word_finished:
                                self.addKeywordToDictionary(aid, kDict, node, key)
                                key = ""
                                node = root
                            else:
                                key += " "
                            continue
                        # if word does not exist in phrase
                        else:
                            key = ""
                            continue  # i += 1

        #iterate through abstract
        key = ""
        if abstract != None:
            for word in abstract.split():
                word = word.lower().strip()

                if word == "social" or word == "media" or word == "socialmedia" or word == "social-media" or word == "social media":
                    containsSocialMedia = True

                flag = False
                childIndex = -1
                # check if word exists in phrase
                for child in node.children:
                    childIndex += 1
                    if word.lower() == child.phrase.lower():
                        flag = True
                        break
                #if word exists in phrase:
                if flag:
                    key += word
                    node = node.children[childIndex]
                    if node.word_finished:
                        self.addKeywordToDictionary(aid, kDict, node, key)
                        key = ""
                        node = root
                    else:
                        key += " "
                    continue
                # if word does not exist in phrase
                else:
                    if node == root:
                        key = ""
                        continue  # i += 1
                    else:
                        node = root
                        key = ""
                        
                        #CASE B
                        flag2 = False
                        childIndex = -1
                        for child in node.children:
                            childIndex += 1
                            if word.lower() == child.phrase.lower():
                                flag2 = True
                                break
                        #if word exists in phrase:
                        if flag2:
                            key += word
                            node = node.children[childIndex]
                            if node.word_finished:
                                self.addKeywordToDictionary(aid, kDict, node, key)
                                key = ""
                                node = root
                            else:
                                key += " "
                            continue
                        # if word does not exist in phrase
                        else:
                            key = ""
                            continue  # i += 1

        if not containsSocialMedia:
            del self.aDict[aid]

        return self.aDict
    

    def writeArticles(self, articleDict):
        with open('articles.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')
            
            writeArticles.writerow(["article_ID","article_title"])
            for aid in articleDict:
                article = articleDict[aid]
                id = int(article.articleID)
                title = str(article.name)
                writeArticles.writerow([id,title])

    def writeArticleKewords(self, articleDict):
        with open('articleKeywords.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            writeArticles.writerow(["article_ID","article_title","keyword_ID","keyword"])
            for aid in articleDict:
                if aid == 830:
                    print("break")
                article = articleDict[aid]
                for keyID in article.keywordDict:
                    keyword = article.keywordDict[keyID]
                    id = int(article.articleID)
                    title = str(article.name)
                    kid = int(keyID)
                    writeArticles.writerow([id,title,kid,keyword])

    def writeArticleCited(self, articleDict):
        with open('articleCited.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            writeArticles.writerow(["article_ID","cited_id"])
            for aid in articleDict:
                article = articleDict[aid]
                for cid in article.cited:
                    id = int(article.articleID)
                    c_id = int(cid)
                    writeArticles.writerow([id,cid])

    def writeArticleCitedBy(self, articleDict):
        with open('articleCitedBy.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            writeArticles.writerow(["article_ID","cited_by_id"])
            for aid in articleDict:
                article = articleDict[aid]
                for cid in article.citedBy:
                    id = int(article.articleID)
                    c_id = int(cid)
                    writeArticles.writerow([id,cid])

    def writeAuthor(self, articleDict):
        with open('articleAuthor.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            writeArticles.writerow(["article_ID","author_name"])
            for aid in articleDict:
                article = articleDict[aid]
                for author_name in article.authorList:
                    writeArticles.writerow([aid,author_name])

    def writeJournal(self, articleDict):
        with open('articleJournal.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')

            writeArticles.writerow(["article_ID","journal", "subject_area", "subject_category"])
            for aid in articleDict:
                article = articleDict[aid]
                writeArticles.writerow([aid, article.journal, article.subject_area, article.subject_category])

    def writeKeywords(self, keywordDict):
        with open('keywords.csv', mode='w', encoding="utf8") as f:
            writeArticles = csv.writer(f, delimiter=",", quotechar='"', quoting=csv.QUOTE_ALL, lineterminator = '\n')
            
            writeArticles.writerow(["article_count","keyword"])
            for keyID in keywordDict:
                keywordNode = keywordDict[keyID]
                count = len(keywordNode.referencedByList)
                writeArticles.writerow([count,keywordNode.keyword])

    def writeKeywords2(self, keywordDict):
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
