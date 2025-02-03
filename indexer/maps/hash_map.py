from indexer.abstract_index import AbstractIndex
import hashlib

class HashMapIndex(AbstractIndex):
    def __init__(self, size=128):
        # initialize size to largest possible number based on number of ASCII characters (128)
        self.size = size
        self.hash_map = self.create_buckets()

    def create_buckets(self):
        buckets = []
        for i in range(self.size):
            buckets.append([])
        return buckets

    def custom_hash_fx(self, term):
        return int(hashlib.sha256(term.encode('utf-8')).hexdigest(), 16)

    def get_bucket(self, term):
        hash_key = (self.custom_hash_fx(term)) % self.size
        bucket = self.hash_map[hash_key]
        return bucket

    def insert(self, term, document_id):
        bucket = self.get_bucket(term)
        for pair in bucket:
            if pair["term"] == term:
                if document_id not in pair["doc_ids"]:
                    pair["doc_ids"].append(document_id)
                return
        bucket.append({"term": term, "doc_ids": [document_id]})

    def search(self, term):
        bucket = self.get_bucket(term)
        for tm, doc_ids in bucket:
            if tm == term:
                return doc_ids
        return []

    def remove(self, term):
        bucket = self.get_bucket(term)
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