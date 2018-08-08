class trie():

    def __init__(self):
        self.next = {}
        self.value = None
        self.addr = None

    def insert(self, word=str(),addr=int()):
        node = self

        for index,letter in enumerate(word):
            if letter in node.next.keys():
                node = node.next[letter]
            else:
                node.next[letter] = trie()
                node = node.next[letter]
            if index == len(word) - 1:
                node.value = word
                node.addr = addr

    def find(self, query=str()):
        node = self

        for index,char in enumerate(query):
            if char in node.next.keys():
                node = node.next[char]
                if index == len(query) - 1:
                    return node
            else:
                return None
