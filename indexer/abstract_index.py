from typing import List, Optional, Any, Generator
from abc import ABC, abstractmethod

#from indexer.trees.bst_node import BSTNode
# test

class AbstractIndex(ABC):
    def __init__(self):
        #self.root: Optional[BSTNode] = None
        pass

    @abstractmethod
    def insert(self, key: Any, value: Any) -> None:
        pass

    @abstractmethod
    def search(self, key: Any) -> List[Any]:
        pass

    @abstractmethod
    def __iter__(self) -> Generator[Any, None, None]:
        pass
