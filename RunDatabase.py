import psycopg2
from Update import UpdateKeywords
from Update import UpdateArticles
from PhraseNode import PhraseNode
#from MultiwayTree import multiwayTree

class PythonApplication2:
    root = PhraseNode('*', -1)

    obj = UpdateKeywords()
    keywordDict = obj.getKeywordDict(root)
    
    #articleDict contains every article and all of its relevant information
    articleDict = {}
    obj2 = UpdateArticles(articleDict)

    try:
        connection = psycopg2.connect(user="stephen",
									    password="stephen",
									    host="localhost",
									    port="5434",
									    database="stephen")    
        cursor = connection.cursor() 

        #--------------------------------------QUERIES--------------------------------------
        #query all articles containing [social media, socialmedia, social-media]
        postgreSQL_select_Query = """SELECT SMA.id, SMA.abstract, SMA.title
                                     FROM public.sma SMA
                                     WHERE (SMA.abstract ~* '(^| |[\(\[@#])(socialmedia|social-media|social media)($| |[\.\?!:;,\)\]])'
                                              OR SMA.title ~* '(^| |[\(\[@#])(socialmedia|social-media|social media)($| |[\.\?!:;,\)\]])')
                                     ORDER BY SMA.id ASC LIMIT 1000"""
        cursor.execute(postgreSQL_select_Query)
        #articleTemp = cursor.fetchall()
        articleTemp = cursor.fetchmany(1000)

        #query cites
        postgreSQL_select_Query = """SELECT SMA.id, C.cites_article_id
                                       FROM public.sma SMA, public.cites C
                                       WHERE SMA.id = C.article_id
                                            AND (SMA.abstract ~* '(^| |[\(\[@#])(socialmedia|social-media|social media)($| |[\.\?!:;,\)\]])'
                                                OR SMA.title ~* '(^| |[\(\[@#])(socialmedia|social-media|social media)($| |[\.\?!:;,\)\]])')
                                       ORDER BY SMA.id ASC LIMIT 1000"""
        cursor.execute(postgreSQL_select_Query)
        #articleTemp = cursor.fetchall()
        citesTemp = cursor.fetchmany(1000)

        #query cited_by
        postgreSQL_select_Query = """SELECT SMA.id, C.cited_by_id
                                        FROM public.sma SMA, public.cited_by C
                                        WHERE SMA.id = C.article_id
	                                        AND (SMA.abstract ~* '(^| |[\(\[@#])(socialmedia|social-media|social media)($| |[\.\?!:;,\)\]])'
	                                            OR SMA.title ~* '(^| |[\(\[@#])(socialmedia|social-media|social media)($| |[\.\?!:;,\)\]])')
                                        ORDER BY SMA.id ASC LIMIT 1000"""
        cursor.execute(postgreSQL_select_Query)
        #articleTemp = cursor.fetchall()
        citedByTemp = cursor.fetchmany(1000)

        #query authors
        postgreSQL_select_Query = """SELECT * FROM public.article_authors
                                     ORDER BY article_id ASC, author_name ASC LIMIT 10000"""
        cursor.execute(postgreSQL_select_Query)
        #authorTemp = cursor.fetchall()
        authorTemp = cursor.fetchmany(1000)

        #query journals
        postgreSQL_select_Query = """SELECT * FROM public.journals
                                     ORDER BY id ASC LIMIT 10000"""
        cursor.execute(postgreSQL_select_Query)
        #journalTemp = cursor.fetchall()
        journalTemp = cursor.fetchmany(1000)

        #--------------------UPDATE ARTICLE DICTIONARY WITH QUERIED INFORMATION--------------------
        for row in articleTemp:
            article_id = row[0]
            abstract = row[1]
            title = row[2]

            #print("art_id: ", article_id)
            #print("art_cited_id: ", cites_article_id)
            #if article_id == 19803:
            #    print("break")

            #instantiate with article id and title
            articleDict = obj2.addArticleToDictionary(article_id, title, True)
            #update article's keyword dictionary
            articleDict = obj2.findKeywordInArticle(root, article_id, title, abstract, keywordDict)
        
        #update article's cites list
        for row in citesTemp:
            article_id = row[0]
            cites_id = row[1]

            print("art_id: ", article_id)
            print("cites_id: ", cites_id)

            #if article_id == 17326 and cites_id == 17327:
            #    print("break")

            articleDict = obj2.updateCited(article_id, "temp_cited_title", cites_id)
            
        #update article's cited_by list
        for row in citedByTemp:
            article_id = row[0]
            cited_by_id = row[1]

            print("art_id: ", article_id)
            print("cited_by_id: ", cited_by_id)

            if article_id == 17326 and cited_by_id == 17327:
                print("break")

            articleDict = obj2.updateCitedBy(article_id, "temp_cited_by_title", cited_by_id)
            
        #update article's author list
        for row in authorTemp:
            article_id = row[0]
            author_name = row[1]

            #print("article_id_auth: ", article_id)
            #print("auth name: ", author_name)

            #if article_id == 19803 and cites_article_id == 215752:
            #    print("break")
            
            articleDict = obj2.updateAuthor(article_id, author_name)

        #update article's journals
        for row in journalTemp:
            article_id = row[0]
            journal_name = row[1]
            subject_area = row[2]
            subject_category = row[3]
            
            articleDict = obj2.updateJournal(article_id, journal_name, subject_area, subject_category)

    except (Exception, psycopg2.Error) as error :
        print ("Error while fetching  data from PostgreSQL", error)

    finally:
        #closing database connection.
        if(connection):
            cursor.close()
            connection.close()
            
            nodeList = []
            for aid in articleDict:
                nodeList.append(articleDict[aid])

            #tree = MultiWayTree(nodeList)

            obj2.writeArticles(articleDict)
            obj2.writeArticleKewords(articleDict)
            obj2.writeArticleCited(articleDict)
            obj2.writeArticleCitedBy(articleDict)
            obj2.writeAuthor(articleDict)
            obj2.writeJournal(articleDict)
            obj2.writeKeywords(keywordDict)
            obj2.writeKeywords2(keywordDict)
            print(len(articleDict))
            print("Closing connection to database")