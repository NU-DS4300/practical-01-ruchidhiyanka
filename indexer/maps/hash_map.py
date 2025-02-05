from indexer.abstract_index import AbstractIndex
import hashlib

class HashMapIndex(AbstractIndex):
    def __init__(self, size=1000):
        # initialize size to large number based on quantity of words/files
        self.size = size
        self.hash_map = self.create_buckets()

    def create_buckets(self):
        # create and return a list of empty buckets for the hash map
        buckets = []
        for i in range(self.size):
            buckets.append([])
        return buckets

    # create custom hash function for reproducibility of hash values
    def custom_hash_fx(self, term):
        return int(hashlib.sha256(term.encode('utf-8')).hexdigest(), 16)

    def get_bucket(self, term):
        # get the bucket based on the hash of the term
        hash_key = (self.custom_hash_fx(term)) % self.size
        bucket = self.hash_map[hash_key]
        return bucket

    def insert(self, term, document_id):
        # insert term and document ID into the appropriate bucket
        bucket = self.get_bucket(term)
        for pair in bucket:
            if pair[0] == term:
                if document_id not in pair[1]:
                    pair[1].append(document_id)
                return
        bucket.append((term, [document_id]))

    def search(self, term):
        # search for a term in the hash map and return associated document IDs
        bucket = self.get_bucket(term)
        print(bucket)
        for tm, doc_ids in bucket:
            if tm == term:
                return doc_ids
        return []

    def remove(self, term):
        # remove a term from the hash map and its associated document IDs
        bucket = self.get_bucket(term)
        for pair in bucket:
            if pair[0] == term:
                bucket.remove(pair)
                return True
        return False

    def __iter__(self):
        # iterate through all terms and document IDs in the hash map
        items = []
        for bucket in self.hash_map:
            for pair in bucket:
                items.append((pair[0], pair[1]))
        return iter(items)

    def print_hashmap(self):
        # return string representation of the entire hash map
        return str(self.hash_map)
