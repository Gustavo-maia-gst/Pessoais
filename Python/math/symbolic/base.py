from abc import ABC, abstractmethod
from numbers import Real


class BaseSymbol(ABC):
    @abstractmethod
    def evaluate(self, x: Real) -> Real:
        raise NotImplementedError

    @abstractmethod
    def derivate(self) -> 'BaseSymbol':
        raise NotImplementedError

    @abstractmethod
    def __repr__(self) -> str:
        raise NotImplementedError

    def simplificate(self) -> 'BaseSymbol':
        return self

    def __add__(self, other):
        return SumOperation(self, other).simplificate()

    def __radd__(self, other):
        return SumOperation(other, self).simplificate()

    def __sub__(self, other):
        return SubOperation(self, other).simplificate()

    def __rsub__(self, other):
        return SubOperation(other, self).simplificate()

    def __mul__(self, other):
        return MultOperation(self, other).simplificate()

    def __rmul__(self, other):
        return MultOperation(other, self).simplificate()

    def __truediv__(self, other):
        return DivOperation(self, other).simplificate()

    def __rtruediv__(self, other):
        return DivOperation(other, self).simplificate()


class Operation(BaseSymbol, ABC):
    def __init__(self, left: BaseSymbol, right: BaseSymbol, symbol: str) -> None:
        self._left = left.simplificate()
        self._right = right.simplificate()
        self._symbol = symbol

    def __repr__(self) -> str:
        return f"({self._left} {self._symbol} {self._right})"


class MultOperation(Operation):
    def __init__(self, left: BaseSymbol, right: BaseSymbol) -> None:
        super().__init__(left, right, "*")

    def derivate(self) -> BaseSymbol:
        from symbols import Constant

        left = self._left
        right = self._right

        if left == 0 or right == 0:
            return Constant(0)

        l_left = left.derivate()
        l_right = right.derivate()

        return l_left * right + l_right * left

    def evaluate(self, x: Real) -> Real:
        return self._left.evaluate(x) * self._right.evaluate(x)

    def simplificate(self) -> 'BaseSymbol':
        from symbols import Constant
        if self._left == 0 or self._right == 0:
            return Constant(0)
        if self._left == 1:
            return self._right
        if self._right == 1:
            return self._left

        return self


class SumOperation(Operation):
    def __init__(self, left: BaseSymbol, right: BaseSymbol) -> None:
        super().__init__(left, right, "+")

    def derivate(self) -> BaseSymbol:
        return self._left.derivate() + self._right.derivate()

    def evaluate(self, x: Real) -> Real:
        return self._left.evaluate(x) + self._right.evaluate(x)

    def simplificate(self) -> 'BaseSymbol':
        from symbols import Constant
        if self._left == 0 and self._right == 0:
            return Constant(0)
        elif self._left == 0:
            return self._right
        elif self._right == 0:
            return self._left

        return self


class SubOperation(Operation):
    def __init__(self, left: BaseSymbol, right: BaseSymbol) -> None:
        super().__init__(left, right, "-")

    def derivate(self) -> BaseSymbol:
        return self._left.derivate() - self._right.derivate()

    def evaluate(self, x: Real) -> 'Real':
        return self._left.evaluate(x) - self._right.evaluate(x)

    def simplificate(self) -> 'BaseSymbol':
        from symbols import Constant
        if self._left == 0 and self._right == 0:
            return Constant(0)
        elif self._left == 0:
            return Constant(-1) * self._right
        elif self._right == 0:
            return self._left

        return self


class DivOperation(Operation):
    def __init__(self, left: BaseSymbol, right: BaseSymbol) -> None:
        super().__init__(left, right, "/")

    def derivate(self) -> BaseSymbol:
        left = self._left
        l_left = left.derivate()
        right = self._right
        l_right = right.derivate()

        return (l_left * right - l_right * left) / (right * right)

    def evaluate(self, x: Real) -> Real:
        return self._left.evaluate(x) / self._right.evaluate(x)

    def simplificate(self) -> 'BaseSymbol':
        if self._right == 0:
            raise ZeroDivisionError()

        if self._right == 1:
            return self._left

        return self
