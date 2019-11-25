
import psycopg2
from Update import UpdateKeywords
from Update import UpdateArticles
from PhraseNode import PhraseNode

class PythonApplication2:
    root = PhraseNode('*', -1)

    obj = UpdateKeywords()
    keywordDict = obj.getKeywordDict(root)
    
    articleDict = {}
    obj2 = UpdateArticles(articleDict)

    try:
        connection = psycopg2.connect(user="stephen",
									  password="stephen",
									  host="localhost",
									  port="5434",
									  database="stephen")    
        cursor = connection.cursor() 

        postgreSQL_select_Query = "SELECT * FROM public.sma ORDER BY id ASC LIMIT 10000"
        cursor.execute(postgreSQL_select_Query)
        #use fetchall to get all articles, use fetchmany(x) to get x number of articles"
        artTemp = cursor.fetchmany(10000)

        postgreSQL_select_Query = "SELECT * FROM public.cites ORDER BY article_id ASC, cites_article_id ASC LIMIT 50000"
        cursor.execute(postgreSQL_select_Query)
        allCites = cursor.fetchmany(50000)
  
        currentCiteID = 0

        #display articles in list
  
        for row in artTemp:
            artCites = []
            while(1):
                print(currentCiteID)
                print(allCites[currentCiteID][0])
                if allCites[currentCiteID][0] < row[0]:
                    currentCiteID += 1
                if allCites[currentCiteID][0] == row[0]:
                    print(allCites[currentCiteID][1])
                    artCites.append(allCites[currentCiteID][1])

                    articleDict = obj2.updateCited(allCites[currentCiteID][0], row[6], allCites[currentCiteID][1])

                    currentCiteID += 1
                else:
                    break


            #TODO create article objects
            print("\nArticle ID =", row[0])
            print("Title =", row[6])
            print("Abstract =", row[3])

            """print("Cites =")
            for i in artCites:
                print(i)"""

            if row[0] == 2:
                print("break")

            articleDict = obj2.addArticleToDictionary(row[0], row[6])
            articleDict = obj2.findKeywordInAbstract(root, row[0], row[6], row[3], keywordDict)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching  data from PostgreSQL", error)

    finally:
        #closing database connection.
       if(connection):
            cursor.close()
            connection.close()
            obj2.writeArticles(articleDict)
            obj2.writeArticleKewords(articleDict)
            obj2.writeArticleCited(articleDict)
            obj2.writeKeywords(keywordDict)
            print(len(articleDict))
            print("Closing connection to database")