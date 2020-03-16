  
class ArticleNode:
    def __init__(self):
        self.title = None             
        self.articleID = None            #int: Article ID
        self.author = None
        self.abstract = None
        self.journal = None
        self.references = []            #int: articleID's of the articles referenced
        self.cited = []
        
        self.successors = []            #Article nodes of the respective references
        self.subTreePredecessors = []   #Root nodes of the respective keywords
        self.predecessors = []          #Article nodes of articles citing current article
        self.visited = False            # BFS checking variable
    def getInfo(self):
        print ("Name: ",self.name)
        print ("KeyWords: ",list(self.keywordDict.values()))           #keywords: lowercase keywords, stripped of whitespaces
        print("Cited",self.cited) 
