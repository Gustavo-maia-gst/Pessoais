from abc import ABC, abstractmethod
from typing import *

class ASTNode(ABC):
    def __init__(self, token) -> None:
        self._children: List[ASTNode] = []
        self._rawToken = token
    
    def addChild(self, node: 'ASTNode'):
        self._children.append(node)