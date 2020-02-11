from ArticleNode import ArticleNode
import csv

class GetArticles():
    """Creates list of articles"""
    
    def __init__(self):
        print("")
        self.articleList = {}

    def createArticleNode(self, aid, title):
        if self.articleList.get(aid):
            article = self.articleList.get(aid)
        else:
            article = ArticleNode(aid)
            article.name = title
        return article

    def getAllArticles(self):
        with open('articles.csv', encoding="utf8") as csv_file:
            readArticles = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in readArticles:
                if line_count == 0:
                    line_count += 1
                else:
                    #print(f'{row[0]}, {row[1]}')

                    article = self.createArticleNode(row[0], row[1])
                    self.articleList[row[0]] = article

                    line_count += 1
            print(f'Processed {line_count} lines.')

    def getKeywords(self):
        #row = [a_id, a_title, keyword_id, keyword_phrase]
        with open('articleKeywords.csv', encoding="utf8") as csv_file:
            readArticles = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in readArticles:
                if line_count == 0:
                    line_count += 1
                else:
                    #print(f'{row[0]}, {row[1]}, {row[2]}, {row[3]}.')

                    article = self.createArticleNode(row[0], row[1])
                    article.keywordList.append(row[2])
                    article.keywordDict[row[2]] = row[3]
                    self.articleList[row[0]] = article

                    line_count += 1
            print(f'Processed {line_count} lines.')

    def getCited(self):
        #row = [a_id, a_title, cited_id]
        with open('articleCited.csv', encoding="utf8") as csv_file:
            readArticles = csv.reader(csv_file, delimiter=',')
            line_count = 0
            for row in readArticles:
                if line_count == 0:
                    line_count += 1
                else:
                    #print(f'{row[0]}, {row[1]}, {row[2]}.')

                    article = self.createArticleNode(row[0], row[1])
                    article.cited.append(row[2])
                    self.articleList[row[0]] = article

                    line_count += 1
            print(f'Processed {line_count} lines.')

    def getArticles(self):
        self.getAllArticles()
        self.getKeywords()
        self.getCited()
        return self.articleList


 #comment this out and add articleDictionary = obj.GetArticles() to get the articles
if __name__ == "__main__":
    obj = GetArticles()
    articleDictionary = obj.getArticles()
    print("article size: " + str(len(articleDictionary)))

    print()
