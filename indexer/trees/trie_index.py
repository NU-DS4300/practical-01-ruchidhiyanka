from indexer.abstract_index import AbstractIndex
from indexer.trees.trie_node import TrieNode

class TrieIndex(AbstractIndex):
    def __init__(self):
        super().__init__()
        self.root: TrieNode = TrieNode()

    def insert(self, key: str, value: int, count: int = 1):
        curr = self.root
        for c in key:
            curr = curr.child[c]
        curr.word_end = True
        curr.values.append(value)
        curr.word_count[value] = curr.word_count.get(value, 0) + count

    def search(self, key: str):
        curr = self.root
        for c in key:
            if c not in curr.child:
                return {"val_count": 0, "total_word_count": 0}
            curr = curr.child[c]

        if curr.word_end:
            return {
                "val_count": len(curr.values),
                "total_word_count": sum(curr.word_count.values()),
            }
        return {"val_count": 0, "total_word_count": 0}

    def __iter__(self):
        def traverse(node: TrieNode, prefix: str):
            if node.word_end:
                yield prefix
            for c in sorted(node.child.keys()):  # Sort to maintain order
                yield from traverse(node.child[c], prefix + c)

        yield from traverse(self.root, "")
    def get_keys_in_order(self):
        """
        Returns a list of keys in ascending order.

        Returns:
            List[Any]: A list of keys in ascending order.
        """
        keys = []
        for node in self:
            keys.append(node)
        return keys