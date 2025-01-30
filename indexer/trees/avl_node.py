from typing import Any, Optional
from indexer.trees.bst_node import BSTNode

class AVLNode(BSTNode):
    """
    AVLNode class represents a node in an AVL tree. It inherits from BSTNode
    adds 1 additional attribute, height, used in balancing the tree.

    Attributes:
        key (Any): The key value stored in the node.
        height (int): The height of the node in the AVL tree.

    Methods:
        __init__(key: Any): Initializes a new instance of the AVLNode class 
        with the given key.
    """
    def __init__(self, key: Any):
        super().__init__(key)
        self.height: int = 1
        self.values = []

    # def add_value(self, value: Any) -> None:
    #     """
    #     Adds a value to the node.
    #
    #     Parameters:
    #         value (Any): The value to be added.
    #
    #     Returns:
    #         None
    #     """
    #     self.values.append(value)

    # def get_values(self):
    #     """
    #     Returns the values stored in the node.
    #
    #     Returns:
    #         list: The values stored in the node.
    #     """
    #     return list(self.values)
