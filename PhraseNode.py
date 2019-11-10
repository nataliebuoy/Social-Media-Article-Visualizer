from ArticleNode import ArticleNode

# https://towardsdatascience.com/implementing-a-trie-data-structure-in-python-in-less-than-100-lines-of-code-a877ea23c1a1
class PhraseNode(object):
    def __init__(self, phrase, pid):
        self.phraseID = pid
        self.phrase = phrase
        self.children = []
        self.word_finished = False  # Is it the last character of the word.
        self.counter = 1 # How many times this character appeared in the addition process

        self.referencedBy = {}
