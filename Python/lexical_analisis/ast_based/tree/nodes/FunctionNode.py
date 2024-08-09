from ASTNode import ASTNode
from ast_based.tree.types import Type

a = Type()

class FunctionNode(ASTNode):
    def __init__(self, rawToken, paramsDefinition, block) -> None:
        super().__init__(self, rawToken)
        self.params = paramsDefinition
        self.block = block
