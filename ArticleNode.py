class ArticleNode:
    def __init__(self,aid):
        self.name =""
        self.articleID = aid
        self.keywordList = []
        self.references = []
        self.authorList = []
        self.successors = []
        self.subTreePredecessors = []
        self.predecessors = []
        self.visited = False

        
