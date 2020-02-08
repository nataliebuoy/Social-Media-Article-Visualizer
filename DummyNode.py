import random
class DummyNode:

    def writeTest(self):
        pid = 0
        DummmyAuthor = ["Adams", "Jameson", "Smith", "Bernard", "Josiah", "Heaster", "Kadrick", "Fisher", "Cherry", "Howe", "Johns", "Carney", "Rollins", "Meyer", "Garza", "Gonzalez", "Bauer", "Jenkins", "Chase"]
        DummyKeys = ["Facebook", "Twitter", "Reddit", "innovative", "sectorial", "importance", "content", "marketing", "Provincial", "knowledge", "research"]
        f = open("test.txt", "w+")
        f.write(" 'ArticleID','CitedArticle','Keywords','Authors'\n")
        for loop in range(100):
            pid += 1
            keywords = random.choices(DummyKeys, k=random.randint(1,4))
            cited = [random.randint(1,100) for x in range(random.randint(1,4))]
            authors = random.choices(DummyAuthor, k=random.randint(1,4))
            keywords = list(set(keywords))
            cited = list(set(cited))
            authors = list(set(authors))
            f.write("'%d'," % pid)
            for item in cited:
                f.write(" '%s'" % item)
            f.write(", '")
            for keys in keywords:
                f.write("%s " % keys)
            f.write(", '")
            for author in authors:
                f.write("%s " % author)
            f.write("'\n")

        f.close()




