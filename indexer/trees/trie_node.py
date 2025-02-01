from typing import List, Optional, Any
#from indexer.abstract_index import AbstractIndex
from collections import defaultdict

class TrieNode:
    def __init__(self):
        self.child = defaultdict(TrieNode)
        self.word_end = False
        self.values = []
        self.word_count = {}


#     def add_value(self, value: Any) -> None:
#         """
#         Adds a value to the node.

#         Parameters:
#             value (Any): The value to be added.

#         Returns:
#             None
#         """
#         self.values.append(value)

#     def get_values(self) -> List[Any]:
#         """
#         Returns the list of values stored in the node.

#         Returns:
#             List[Any]: The list of values.
#         """
#         return self.values

#     def get_values_count(self) -> int:
#         """
#         Returns the number of values stored in the node.

#         Returns:
#             int: The number of values stored in the node.
#         """
#         return len(self.values)