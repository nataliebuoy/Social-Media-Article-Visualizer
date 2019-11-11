class KeywordNode:
    def __init__(self,kid,keyword):
        self.keywordID = kid
        self.keyword = keyword
        self.referencedByList = []