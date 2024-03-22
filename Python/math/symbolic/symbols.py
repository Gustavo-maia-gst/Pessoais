from base import BaseSymbol
from typing import Any
from numbers import Real
from abc import ABC, abstractmethod
import math


class Constant(BaseSymbol):
    def __init__(self, value: Real) -> None:
        self.value = value

    def evaluate(self, x: Real) -> Real:
        return self.value

    def derivate(self) -> 'Constant':
        return self

    def __repr__(self):
        if self.value == math.e:
            return 'e'
        return str(self.value)

    def __eq__(self, other):
        return self.value == other


class Variable(BaseSymbol):
    def __init__(self, symbol: str = "x"):
        self.symbol = symbol

    def evaluate(self, x: Real) -> Real:
        return x

    def derivate(self) -> Any:
        return Constant(1)

    def __repr__(self) -> str:
        return self.symbol


class Function(BaseSymbol, ABC):
    def __init__(self, inner: Any) -> None:
        self.inner = inner

    @abstractmethod
    def _self_derivate(self) -> 'BaseSymbol':
        raise NotImplementedError

    def derivate(self) -> 'BaseSymbol':
        return self._self_derivate().simplificate() * self.inner.derivate().simplificate()
