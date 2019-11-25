class ArticleNode:
    def __init__(self,aid,title):
        self.articleTitle = title
        self.articleID = aid
        self.keywordList = [] #contains ids
        self.keywordDict = {} #contains ids and nodes
        self.cited = [] #contains article ids

        self.successors = [] #cited as article nodes
        self.subTreePredecessors = []
        self.predecessors = [] #keyword nodes
        self.visited = False