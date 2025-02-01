
from indexer.abstract_index import AbstractIndex
from indexer.trees.trie_node import TrieNode
class TrieIndex(AbstractIndex):
    def __init__(self):
        super().__init__()
        self.root: TrieNode = TrieNode()

    def insert(self, key: str, value: int, count: int = 1) -> None:
        curr = self.root
        for c in key:
            index = ord(c) - ord('a')
            if curr.child[index] is None:
                curr.child[index] = TrieNode()
            curr = curr.child[index]

        curr.word_end = True
        curr.values.append(value)
        curr.word_count[value] = curr.word_count.get(value, 0) + count

    def search(self, key: str):
        curr = self.root
        for c in key:
            index = ord(c) - ord('a')
            if curr.child[index] is None:
                return {"val_count": 0, "total_word_count": 0}
            curr = curr.child[index]

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
            for i in range(26):
                if node.child[i] is not None:
                    yield from traverse(node.child[i], prefix + chr(i + ord('a')))

        yield from traverse(self.root, "")

    def get_keys_in_order(self):
        """
        Returns a list of keys in ascending order.

        Returns:
            List[Any]: A list of keys in ascending order.
        """
        keys = []
        for node in self:
            keys.append(node.key)
        return keys