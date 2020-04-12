import csv

class GetAuthors():
    
    def __init__(self):
        print("")

        self.authorDict = {}

    def getAuthor(self):
        #row = [article_ID, author_name]
        with open('articleAuthor.csv', encoding="utf8") as csv_file:
           
            readArticles = csv.reader(csv_file, delimiter=',')
            
            for row in readArticles:
                author = row[1].lower()
                articles = row[0].lower()
                  
                if author not in self.authorDict.keys():
                    update = [articles]
                    self.authorDict.update({author: update})
                else:
                    update = self.authorDict.get(author)
                    update.append(articles)
                    self.authorDict.update({author: update})

            # for author in self.authorDict.keys():
            #     print("Author is: " + author)
            #     print("Articles are: ")
            #     print(self.authorDict[author])
            #     print("")


        # Returns article IDs of articles written by author (matches full author name or by last name)
    def authorSearch(self, authorName, authorDict):

        authorName = authorName.lower()
        lastName = authorName.split(" ")[-1]  
        firstName = authorName.split(" ")[0]
        
        # Exact full name match
        if authorName in self.authorDict:
           print("Articles by: " + authorName)
           print(authorDict.get(authorName))
           return(authorDict.get(authorName))

        else:
            for authorName in self.authorDict:    
                # Middle initial ignored, first and last name match           
                if authorName.endswith(lastName) and authorName.startswith(firstName):
                    print("Articles by: " + authorName)
                    print(authorDict.get(authorName))
                    return(authorDict.get(authorName))
                    
                # When only the last name is searched, return articles by authors with the last name
                elif authorName.endswith(lastName) and firstName == lastName:
                    print("Articles by name: " + authorName)
                    print(authorDict.get(authorName))
                    return(authorDict.get(authorName))
                    
        print("No articles by this author!")
        return None

    def getAuthors(self):
        self.getAuthor()
        return self.authorDict


if __name__ == "__main__":

    obj = GetAuthors()
    authorDictionary = obj.getAuthors()

    # authorName = "Ronald Burt"
    # obj.authorSearch(authorName, authorDictionary)

    #print("author count: " + str(len(authorDictionary)))
