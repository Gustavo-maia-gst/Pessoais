from ASTNode import ASTNode

class ProgramNode(ASTNode):
    def __init__(self, rawToken, funcDefinitions) -> None:
        super().__init__(rawToken)
        self._children = funcDefinitions
