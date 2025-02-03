from typing import List, Optional, Any
#from indexer.abstract_index import AbstractIndex
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.child = defaultdict(TrieNode)
        self.word_end = False
        self.values = []