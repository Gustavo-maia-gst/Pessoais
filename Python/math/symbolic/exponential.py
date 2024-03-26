from base import BaseSymbol
from symbols import Function, Constant, Variable
from typing import Any
from numbers import Real
import math


class Logarithm(Function):
    def __init__(self, base: Constant | Real, inner: Any = Variable("x")):
        super().__init__(inner)
        self.base = base

    def evaluate(self, x: Real) -> Real:
        return math.log(self.inner.evaluate(x), self.base.evaluate(x))

    def _self_derivate(self) -> 'BaseSymbol':
        if self.base == math.e:
            return Constant(1) / self.inner

        return Constant(1) / (Logarithm(math.e, self.base) * self.inner)

    def simplificate(self) -> 'BaseSymbol':
        if self.base == self.inner:
            return Constant(1)

        return self

    def __repr__(self) -> str:
        representation = f'log{self.base}' if self.base != math.e else 'ln'
        return f'{representation}({self.inner})'


class Exponential(BaseSymbol):
    def __init__(self, base: 'BaseSymbol', inner: Any = Variable("x")):
        self.inner = inner
        self.base = base

    def evaluate(self, x: Real) -> Real:
        return self.base.evaluate(x) ** self.inner.evaluate(x)

    def derivate(self) -> 'BaseSymbol':
        g = self.inner * Logarithm(math.e, self.base)
        deriv = self * g.derivate()
        print(deriv)
        return deriv

    def simplificate(self) -> 'BaseSymbol':
        if self.base == 0:
            return Constant(0)
        if self.base == 1 or self.inner == 0:
            return Constant(1)
        if self.inner == 1:
            return self.base

        return self

    def __repr__(self) -> str:
        return f'{self.base}^({self.inner})'
