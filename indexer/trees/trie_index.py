
from indexer.abstract_index import AbstractIndex
from indexer.trees.trie_node import TrieNode
class TrieIndex(AbstractIndex):
    def __init__(self):
        super().__init__()
        self.root: TrieNode = TrieNode()

    def insert(self, word: str, doc_id: int, count: int = 1) -> None:
        curr = self.root
        for c in word:
            index = ord(c) - ord('a')
            if curr.child[index] is None:
                curr.child[index] = TrieNode()
            curr = curr.child[index]

        curr.word_end = True
        curr.document_ids.add(doc_id)
        curr.word_count[doc_id] = curr.word_count.get(doc_id, 0) + count

    def search(self, word: str) -> Dict[str, Any]:
        curr = self.root
        for c in word:
            index = ord(c) - ord('a')
            if curr.child[index] is None:
                return {"document_count": 0, "total_word_count": 0}
            curr = curr.child[index]

        if curr.word_end:
            return {
                "document_count": len(curr.document_ids),
                "total_word_count": sum(curr.word_count.values()),
            }
        return {"document_count": 0, "total_word_count": 0}

    def __iter__(self) -> Generator[str, None, None]:
        def traverse(node: TrieNode, prefix: str) -> Generator[str, None, None]:
            if node.word_end:
                yield prefix
            for i in range(26):
                if node.child[i] is not None:
                    yield from traverse(node.child[i], prefix + chr(i + ord('a')))

        yield from traverse(self.root, "")