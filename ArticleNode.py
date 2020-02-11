class ArticleNode:
    def __init__(self,aid):
        self.name =""                   #name
        self.articleID = aid            #int: Article ID
        self.keywordList = []           #keywords: lowercase keywords, stripped of whitespaces
        self.references = []            #int: articleID's of the articles referenced
        self.keywordDict = {}
        self.cited = []
        
        self.successors = []            #Article nodes of the respective references
        self.subTreePredecessors = []   #Root nodes of the respective keywords
        self.predecessors = []          #Article nodes of articles citing current article
        self.visited = False            # BFS checking variable

        
