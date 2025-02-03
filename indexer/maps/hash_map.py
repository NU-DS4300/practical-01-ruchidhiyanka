from indexer.abstract_index import AbstractIndex

class HashMapIndex(AbstractIndex):
    def __init__(self, size=128):
        # initialize size to highest possible number based on number of ASCII characters (128)
        self.size = size
        self.hash_map = self.create_buckets()

    def create_buckets(self):
        buckets = []
        for i in range(self.size):
            buckets.append([])
        return buckets

    def _get_bucket(self, term):
        hash_key = hash(term) % self.size
        bucket = self.hash_map[hash_key]
        return bucket

    def insert(self, term, document_id):
        bucket = self._get_bucket(term)
        for pair in bucket:
            if pair["term"] == term:
                if document_id not in pair["doc_ids"]:
                    pair["doc_ids"].append(document_id)
                return
        bucket.append({"term": term, "doc_ids": [document_id]})

    def search(self, term):
        bucket = self._get_bucket(term)
        for tm, doc_ids in bucket:
            if tm == term:
                return doc_ids
        return []

    def remove(self, term):
        bucket = self._get_bucket(term)
        for pair in bucket:
            if pair[0] == term:
                bucket.remove(pair)
                return True
        return False

    def __iter__(self):
        items = []
        for bucket in self.hash_map:
            for pair in bucket:
                items.append((pair["term"], pair["doc_ids"]))
        return iter(items)

    def print_hashmap(self):
        return str(self.hash_map)