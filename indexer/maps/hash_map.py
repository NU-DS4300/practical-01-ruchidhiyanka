from indexer.abstract_index import AbstractIndex

class HashMapIndex(AbstractIndex):
    #
    def __init__(self):
        super().__init__()
        self.hash_map = {}

    def add(self, term, document_id):
        pass

    def search(self, term):
        pass

    def remove(self, term):
        pass