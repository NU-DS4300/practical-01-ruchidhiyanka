from typing import List, Optional, Any

from indexer.trees.bst_index import BinarySearchTreeIndex
from indexer.trees.avl_node import AVLNode

class AVLTreeIndex(BinarySearchTreeIndex):
    """
    An AVL Tree implementation of an index that maps a key to a list of values.
    AVLTreeIndex inherits from BinarySearchTreeIndex meaning it automatically
    contains all the data and functionality of BinarySearchTree.  Any
    functions below that have the same name and param list as one in 
    BinarySearchTreeIndex overrides (replaces) the BSTIndex functionality. 

    Methods:
        insert(key: Any, value: Any) -> None:
            Inserts a new node with key and value into the AVL Tree
    """
    
    def __init__(self):
       super().__init__()
       self.root: Optional[AVLNode] = None

    def _height(self, node: Optional[AVLNode]) -> int:
        """
        Calculate the height of the given AVLNode.

        Parameters:
        - node: The AVLNode for which to calculate the height.

        Returns:
        - int: The height of the AVLNode. If the node is None, returns 0.
        """
        
        # TODO: make sure to update height appropriately in the
        # recursive insert function.
        
        if not node:
            return 0
        return node.height

    def tree_height(self) -> int:
        """
        User method to calculate the height of the AVL.

        Returns:
            int: The height of the AVL tree.
        """
        return self._tree_height(self.root)

    def _rotate_right(self, y: AVLNode) -> AVLNode:
        """
        Performs a right rotation on the AVL tree.

        Args:
            y (AVLNode): The node to be rotated.

        Returns:
            AVLNode: The new root of the rotated subtree.
        """
        
        # TODO: implement the right rotation for AVL Tree

        x = y.left
        z = x.right

        #rotate:
        x.right = y
        y.left = z

        #update heights (the height of its tallest child plus one)
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        x.height = max(self._height(x.left), self._height(x.right)) + 1

        return x

    def _rotate_left(self, x: AVLNode) -> AVLNode:
        """
        Rotate the given node `x` to the left.
        Args:
            x (AVLNode): The node to be rotated.
        Returns:
            AVLNode: The new root of the subtree after rotation.
        """
        
        # TODO: implement the left rotation for AVL Tree

        y = x.right
        z = y.left

        # rotate:
        y.left = x
        x.right = z

        # update heights (the height of its tallest child plus one)
        y.height = max(self._height(y.left), self._height(y.right)) + 1
        x.height = max(self._height(x.left), self._height(x.right)) + 1

        return y

    def _insert_recursive(self, current: Optional[AVLNode], key: Any, value: Any) -> AVLNode:
        """
        Recursively inserts a new node with the given key and value into the AVL tree.
        Args:
            current (Optional[AVLNode]): The current node being considered during the recursive insertion.
            key (Any): The key of the new node.
            value (Any): The value of the new node.
        Returns:
            AVLNode: The updated AVL tree with the new node inserted.
        """
        # TODO: Implement a proper recursive insert function for an
        # AVL tree including updating height and balancing if a
        # new node is inserted. 
        
        # TODO: Remove or comment out this line once you've implemented
        # the AVL insert functionality 
        #current = super()._insert_recursive(current, key, value)

        # normal BST insert
        if not current:
            node = AVLNode(key)
            node.add_value(value)
            return node
        elif key < current.key:
            current.left = self._insert_recursive(current.left, key, value)
        elif key > current.key:
            current.right = self._insert_recursive(current.right, key, value)
        else:
            current.add_value(value)
            return current

        # update height of the new node
        current.height = 1 + max(self._height(current.left), self._height(current.right))

        #check balance of the newly added node (left node - right node)
        balance = self._height(current.left) - self._height(current.right)

        # right right case
        if balance < -1 and key > current.right.key:
            return self._rotate_left(current)

        # left left case
        if balance > 1 and key < current.left.key:
            return self._rotate_right(current)

        # right left case
        if balance < -1 and key < current.right.key:
            current.right = self._rotate_right(current.right)
            return self._rotate_left(current)

        # left right case
        if balance > 1 and key > current.left.key:
            current.left = self._rotate_left(current.left)
            return self._rotate_right(current)

        return current

    def insert(self, key: Any, value: Any) -> None:
        """
         User method to insert a key-value pair into the AVL tree. If the key exists, the
         value will be appended to the list of values in the node. 

        Parameters:
            key (Any): The key to be inserted.
            value (Any): The value associated with the key.

        Returns:
            None
        """
        if self.root is None:
            self.root = AVLNode(key)
            self.root.add_value(value)
        else:
            self.root = self._insert_recursive(self.root, key, value)

    def _inorder_traversal(self, current: Optional[AVLNode], result: List[Any]) -> None:
        if current is None:
            return
        
        self._inorder_traversal(current.left, result)
        result.append(current.key)
        self._inorder_traversal(current.right, result)
   
    def get_keys(self) -> List[Any]:
        keys: List[Any] = []
        self._inorder_traversal(self.root, keys)
        return keys

    # def _search_recursive(self, node: Optional[AVLNode], key: Any) -> List[Any]:
    #     """
    #     Recursively searches for a node with the given key and value.
    #     Args:
    #         node (Optional[AVLNode]): The current node being considered during the search.
    #         key (Any): The key of the target node.
    #     Returns:
    #         List[Any]: The list of values associated with the key, or None if not found.
    #     """
    #
    #    # if reached leaf node, then key is not found
    #     if not node:
    #         return None
    #     # if value matches the key, return the values associated with the key
    #     if node.key == key:
    #         return node.get_values()
    #     # if node's value is less than target value, search the right subtree of the key
    #     # otherwise, search the left
    #     if node.key < key:
    #         return self._search_recursive(node.right, key)
    #     else:
    #         return self._search_recursive(node.left, key)

    # def search(self, key: Any) -> List[Any]:
    #     """
    #     User method to search for a key in the AVL tree.
    #
    #     Parameters:
    #         key (Any): The target key.
    #
    #     Returns:
    #         List[Any]: The list of values associated with the key, or None if not found.
    #     """
    #     return self._search_recursive(self.root, key)


    # def _count_nodes(self, node: Optional[AVLNode]) -> int:
    #     """
    #     Recursively counts the number of nodes in the AVL tree.
    #     Parameters:
    #     - node (Optional[AVLNode]): The root node of the AVL tree.
    #     Returns:
    #     - int: The number of nodes in the AVL tree.
    #     """
    #
    #     if node is None:
    #         return 0
    #     return 1 + self._count_nodes(node.left) + self._count_nodes(node.right)

    # def count_nodes(self) -> int:
    #     """
    #     User method to count the number of nodes in the AVL.
    #
    #     Returns:
    #         int: The number of nodes in the AVL tree.
    #     """
    #     return self._count_nodes(self.root)
