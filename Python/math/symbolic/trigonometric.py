from numbers import Real
from typing import Any
import math
from base import BaseSymbol
from symbols import Function, Variable


class Sine(Function):
    def __init__(self, inner: Any = Variable('x')):
        super().__init__(inner)

    def evaluate(self, x: Real) -> Real:
        return math.sin(x)

    def _self_derivate(self) -> 'BaseSymbol':
        return Cosine(self.inner)

    def __repr__(self) -> str:
        return f'sin({self.inner})'


class Cosine(Function):
    def __init__(self, inner: Any = Variable('x')):
        super().__init__(inner)

    def evaluate(self, x: Real) -> Real:
        return math.cos(x)

    def _self_derivate(self) -> 'BaseSymbol':
        return -1 * Sine(self.inner)

    def __repr__(self) -> str:
        return f'cos({self.inner})'
