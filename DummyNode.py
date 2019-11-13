import random
class DummyNode:

    def writeTest(self):
        pid = 0
        DummyKeys = ["Facebook", "Twitter", "Reddit", "innovative", "sectorial", "importance", "content", "marketing", "Provincial", "knowledge", "research"]
        f = open("test.txt", "w+")
        f.write(" 'ArticleID','CitedArticle','Keywords'\n")
        for loop in range(100):
            pid += 1
            keywords = random.choices(DummyKeys, k=random.randint(1,4))
            cited = [random.randint(1,100) for x in range(random.randint(1,4))]
            keywords = list(set(keywords))
            cited = list(set(cited))
            f.write("'%d'," % pid)
            for item in cited:
                f.write(" '%s'" % item)
            f.write(", '")
            for keys in keywords:
                f.write("%s " % keys)
            f.write("'\n")

        f.close()




