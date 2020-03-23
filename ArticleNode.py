class ArticleNode:
    def __init__(self,aid,name):
        self.name = name                #name
        self.articleID = aid            #int: Article ID
        self.abstract = None
        self.authorList = []
        self.cited = []
        self.references = []            #int: articleID's of the articles referenced
        self.citedBy = []
        self.journal = None
        self.subject_area = None
        self.subject_category = None
        self.keywordDict = {}
        self.keywordList = []           #keywords: lowercase keywords, stripped of whitespaces
    
        self.contains_social_media = False
        
        self.successors = []            #Article nodes of the respective references
        self.subTreePredecessors = []   #Root nodes of the respective keywords
        self.predecessors = []          #Article nodes of articles citing current article
        self.visited = False            # BFS checking variable

    def getInfo(self):
        print ("Name: ",self.name)
        print ("KeyWords: ",list(self.keywordDict.values()))           #keywords: lowercase keywords, stripped of whitespaces
        print("Cited",self.cited)           #int: articleID's of the articles referenced
        
