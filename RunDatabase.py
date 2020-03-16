import psycopg2
from ArticleNode import ArticleNode
from Update import UpdateKeywords
from Update import UpdateArticles
from PhraseNode import PhraseNode

class PythonApplication2:



    def getIdsFromKeyword(kw):
         
            try:
                connection = psycopg2.connect(user="stephen",
									            password="stephen",
									            host="localhost",
									            port="5434",
									            database="stephen")    
                cursor = connection.cursor()

                postgreSQL_select_Query = "SELECT * FROM public.sma WHERE abstract ILIKE '%social media%' AND abstract ILIKE "
                postgreSQL_select_Query = postgreSQL_select_Query + "'%" + kw + "%'"
                print (postgreSQL_select_Query)
                cursor.execute(postgreSQL_select_Query)
                #use fetchall() to get all articles, use fetchmany(x) to get x number of articles"
                #artTemp = cursor.fetchall()
                artTemp = cursor.fetchall()
                keywordList = []
                i = 0
                for row in artTemp:
                    #print()
                    #print(row[0])
                    #print(row[3])
                    #print(len(artTemp))
                    newNode = ArticleNode()
                    newNode.articleId = row[0]
                    newNode.abstract = row[3]
                    newNode.title = row[6]
                    newNode.journal = row[7]
                    print("art id added: ", newNode.articleId)
                    #print("Journal added: ", newNode.journal)
                    i += 1   
                    keywordList.append(newNode)

                
            except (Exception, psycopg2.Error) as error :
                print ("Error while fetching  data from PostgreSQL", error)

        
            print("total count: ", i)
            return keywordList

    def getIdsFromAuthor(author):

        try:
                connection = psycopg2.connect(user="stephen",
									            password="stephen",
									            host="localhost",
									            port="5434",
									            database="stephen")    
                cursor = connection.cursor()

                postgreSQL_select_Query = "SELECT * FROM public.sma WHERE abstract ILIKE '%social media%'"
                #print (postgreSQL_select_Query)
                cursor.execute(postgreSQL_select_Query)
                #use fetchall() to get all articles, use fetchmany(x) to get x number of articles"
                artTemp = cursor.fetchall()
                authorList = []
   
                for row in artTemp:

                    postgreSQL_select_Query = "SELECT * FROM public.article_authors WHERE author_name LIKE "
                    postgreSQL_select_Query = postgreSQL_select_Query + "'%" + author + "%' AND article_id = " + str(row[0])
                    #print (postgreSQL_select_Query)
                    cursor.execute(postgreSQL_select_Query)
                    authors = cursor.fetchall()
                    newNode = ArticleNode()
                    for a in authors:
                        newNode.author = a[1]
                        newNode.articleId = a[0]
                        newNode.abstract = row[3]
                        newNode.title = row[6]
                        newNode.journal = row[7]

                        #print(newNode.author)
                        authorList.append(newNode)

                
        except (Exception, psycopg2.Error) as error :
                print ("Error while fetching  data from PostgreSQL", error)



        return authorList

    def getSubAreas(idList):
        categoryList = []
        try:
                connection = psycopg2.connect(user="stephen",
									            password="stephen",
									            host="localhost",
									            port="5434",
									            database="stephen")    
                cursor = connection.cursor()

                subAreas = {}
                
                for article in idList:
                    
                    if article.journal is not None:
                        postgreSQL_select_Query = "SELECT * FROM public.journals WHERE id = "
                        postgreSQL_select_Query = postgreSQL_select_Query + str(article.journal)
                        print (postgreSQL_select_Query)
                        cursor.execute(postgreSQL_select_Query)
                        #use fetchall() to get all articles, use fetchmany(x) to get x number of articles"
                        artTemp = cursor.fetchall()
                        for (id,name, area,cat,region) in artTemp:
                            print ("area: ",area)
                            if area is None:
                                if subAreas.get("Undefined") is None:
                                    subAreas.update({"Undefined": 1})
                                else:
                                    subAreas.update({"Undefined":subAreas.get("Undefined")+1})
                            else:
                                if subAreas.get(area) is None:
                                    subAreas.update({area: 1})
                                else:
                                    subAreas.update({area:subAreas.get(area)+1})

                    else:
                         if subAreas.get("Undefined") is None:
                            subAreas.update({"Undefined": 1})
                         else:
                            subAreas.update({"Undefined":subAreas.get("Undefined")+1})

        except (Exception, psycopg2.Error) as error :
                print ("Error while fetching  data from PostgreSQL", error)
                        
        print(subAreas)
        return subAreas
    
    def getCategory(areaList):
        for area in areaList:
            print( area)


        return 0

    idList = getIdsFromKeyword("instagram")
    #getIdsFromAuthor("z")
    areaList = getSubAreas(idList)
    getCategory(areaList)

    
        

        

    

    
