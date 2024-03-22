from numbers import Real
from symbols import Function, Variable, Constant
from typing import Any
from base import BaseSymbol


class Monomial(Function):
    def __init__(self, coefficient: Real, power: Real, inner: Any = Variable('x')) -> None:
        super().__init__(inner)
        self.coefficient = coefficient
        self.power = power

    def evaluate(self, x: Real) -> Real:
        return self.coefficient * (self.inner.evaluate(x) ** self.power)

    def _self_derivate(self) -> 'BaseSymbol':
        if self.coefficient == 0:
            return Constant(0)
        if self.power == 1:
            return Constant(self.coefficient)

        return Monomial(self.coefficient * self.power, self.power-1, self.inner)

    def simplificate(self) -> 'BaseSymbol':
        if self.coefficient == 0:
            return Constant(0)
        if self.power == 0:
            return Constant(self.coefficient)

        return self

    def __repr__(self):
        coef = self.coefficient if self.coefficient != 1 else ''
        power = f'^{str(self.power)}' if self.power != 1 else ''

        return f'{coef}{self.inner}{power}'
