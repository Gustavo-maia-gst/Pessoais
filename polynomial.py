from numbers import Real
from typing import Iterable


class Monomial:
    def __init__(self, coef: Real, power: int) -> None:
        self.coef = coef
        if power < 0:
            self.power = 0
        else:
            self.power = power

    def evaluate(self, x: Real) -> Real:
        return self.coef * (x ** self.power)
    
    def derivate(self) -> 'Monomial':
        return self.__class__(self.coef * self.power, self.power - 1)

    def __repr__(self) -> str:
        return f'{self.coef}X{self.power}'

    def __mul__(self, other: 'Monomial | Real') -> 'Monomial':
        try:
            if isinstance(other, Real):
                return self.__class__(self.coef * other, self.power)

            coef = self.coef * other.coef
            power = self.power + other.power
            return self.__class__(coef, power)

        except AttributeError:
            raise TypeError("Can only multiply a monomial with an another monomial")

    def __truediv__(self, other: 'Monomial') -> 'Monomial':
        try:
            if isinstance(other, Real):
                return self.__class__(self.coef / other, self.power)

            coef = self.coef / other.coef
            power = self.power - other.power
            if power < 0:
                raise ValueError(f"Cannot divide a monomial of degree {self.power} by a monomial with degree {other.power}")

            return self.__class__(coef, power)

        except AttributeError:
            raise TypeError("Can only divide a monomial with an another monomial with lower degree")

    def __add__(self, other: 'Monomial') -> 'Monomial':
        try:
            if self.power != other.power:
                raise ValueError("Cannot add monomials of diferent powers")

            coef = self.coef + other.coef
            return self.__class__(coef, self.power)

        except AttributeError:
            raise TypeError("Can only add a monomial with an another monomial")

    def __sub__(self, other: 'Monomial') -> 'Monomial':
        try:
            if self.power != other.power:
                raise ValueError("Cannot subtract monomials of diferent powers")

            coef = self.coef - other.coef
            return self.__class__(coef, self.power)

        except AttributeError:
            raise TypeError("Can only subtract a monomial with an another monomial")


class RepresentationError(Exception):
    def __init__(self) -> None:
        msg = 'Wrong format, use the following format for representing: {coef}X{power} + {coef}X{power}; ex: 2X2 +5X'
        super().__init__(self, msg)


class Polynomial:
    def __init__(self, representation: str) -> None:
        def read_term(term: str) -> Monomial:
            if not 'X' in term:
                return Monomial(float(term), 0)
            
            left, right = term.split('X')
            if left:
                coef = float(left)
            else:
                coef = 1
            if right:
                power = int(right)
            else:
                power = 1
            return Monomial(coef, power)
        

        self.terms = {}

        for term in representation.upper().split():
            try:
                mono = read_term(term)
                self.terms[mono.power] += mono
            except KeyError:
                self.terms[mono.power] = mono
            except ValueError:
                raise RepresentationError()

    @property
    def degree(self) -> int:
        if not self.terms:
            return 0
        return max(self.terms.keys())
    
    def evaluate(self, x: Real) -> Real:
        s = 0
        for term in self.terms.values():
            s += term.evaluate(x)

        return s

    def derivate(self) -> 'Polynomial':
        derivative = ''
        for key in self.terms:
            if key > 0:
                derivative += f'{str(self.terms[key].derivate())} '
        derivative.strip()
        return self.__class__(derivative)

    def _find_root(self, precision: float) -> Real | None:
        maximum = 0
        for _, term in self:
            if abs(term.coef) > maximum:
                maximum = abs(term.coef)
    
        bl = -maximum
        br = maximum
        derivative = self.derivate()
        r_x = bl
        l_x = br

        while True:
            if not r_x is None:
                r_guess = self.evaluate(r_x)
                if abs(r_guess) < precision:
                    return r_x
                r_x = r_x - (r_guess / derivative.evaluate(r_x))
                if not bl <= r_x <= br:
                    r_x = None

            if not l_x is None:
                l_guess = self.evaluate(l_x)
                if abs(l_guess) < precision:
                    return l_x
                l_x = l_x - (l_guess / derivative.evaluate(l_x))
                if not bl <= l_x <= br:
                    l_x = None

            if l_x is None and r_x is None:
                return None
    
    @staticmethod
    def roots(poly: 'Polynomial', precision: float) -> list:
        if poly.degree == 2:
            a, b, c = poly[2].coef, poly[1].coef, poly[0].coef
            delta = b ** 2 - 4 * a * c
            
            if -5 * precision <= delta <= 5 * precision:
                delta = 0

            if delta < 0:
                return []

            x1 = (-b + (delta ** (1/2))) / (2 * a)
            x2 = (-b - (delta ** (1/2))) / (2 * a)

            return [x1, x2]

        r = poly._find_root(precision)
        if not r:
            return None

        R = Polynomial(f'x {r * (-1)}')

        other_roots = Polynomial.roots(poly / R, precision)

        if other_roots:
            return [r] + other_roots
        else:
            return [r]

    def mult(self, other: 'Polynomial') -> 'Polynomial':
        result = self.__class__('0x1')

        for _, mono in self:
            for _, term in other:
                result += self.__class__(str(term * mono))

        return result

    def __add__(self, other: 'Polynomial') -> 'Polynomial':
        result = self.__class__(str(self))
        for deg, term in other:
            try:
                result[deg] += term
            except KeyError:
                result[deg] = term
            if result[deg].coef == 0:
                del result[deg]
        return result

    def __sub__(self, other: 'Polynomial') -> 'Polynomial':
        result = self.__class__(str(self))
        for deg, term in other:
            try:
                result[deg] -= term
            except KeyError:
                result[deg] = term * (-1)
            if result[deg].coef == 0:
                del result[deg]
        return result

    def __mul__(self, other: 'Polynomial | Monomial | Real') -> 'Polynomial':
        terms = []
        for deg, term in self:
            terms.append(term * other)

        representation = str(terms[0])
        for term in terms[1:]:
            representation += f' {str(term)}'

        return self.__class__(representation)

    def __truediv__(self, other: 'Polynomial') -> 'Polynomial':
        try:
            if other.degree >= self.degree:
                raise ValueError('Can only divide a polynomial by another with lower degree')

            R = self.__class__(str(self))
            Q = self.__class__('0X1')

            while True:
                a = R[R.degree] / other[other.degree]
                Q += self.__class__(str(a))
                R -= other * a
                if R.degree < other.degree:
                    break

            return Q
        except AttributeError:
            raise TypeError('Can only divide a polynomial by another')

    def __repr__(self) -> str:
        return f'Polynomial({str(self)})'

    def __str__(self) -> str:
        terms = [str(self.terms[key]) for key in self.terms]

        string = terms[0]
        for term in terms[1:]:
            string += f' {term}'

        return string

    def __getitem__(self, deg: int) -> Monomial:
        return self.terms[deg]

    def __setitem__(self, deg: int, term: Monomial) -> None:
        self.terms[deg] = term

    def __delitem__(self, deg: int) -> None:
        del self.terms[deg]

    def __iter__(self) -> Iterable:
        return iter(sorted(self.terms.items(), key=lambda t: t[0], reverse=True))


if __name__ == '__main__':
    representation = str(input('Digite o polinômio: '))
    p = Polynomial(representation)
    precision = int(input(f'Qual a precisão desejada (10 ^ -i): '))
    precision = 10 ** (-precision)
    roots = Polynomial.roots(p, precision=precision)
    roots = [round(x, 5) for x in roots]
    print(f'Essas são as raízes reais encontradas: {roots}')
