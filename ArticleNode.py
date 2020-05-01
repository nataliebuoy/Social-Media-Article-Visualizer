class ArticleNode:
    def __init__(self):
        self.title = None             
        self.articleId = None            #int: Article ID
        self.author = None
        self.abstract = None
        self.journal = None
        self.references = []            #int: articleID's of the articles referenced
        self.cited = []
        self.area = None
        self.subCat = None
        
        self.successors = []            #Article nodes of the respective references
        self.subTreePredecessors = []   #Root nodes of the respective keywords
        self.predecessors = []          #Article nodes of articles citing current article
        self.visited = False            # BFS checking variable
    def getInfo(self):
        return(self.articleId)
    def getSubCat(self):
        return (self.subCat)
    def getReferences(self):
        return (self.references)
    def getTitle(self):
        return(self.title)

