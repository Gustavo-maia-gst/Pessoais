from numbers import Complex, Real
import math
from trigonometric import half_cis


class ComplexNumber(Complex):
    precision = 4

    def __init__(self, real: Real, imag: Real) -> None:
        self.__real = real
        self.__imag = imag

    @property
    def real(self) -> Real:
        return self.__real

    @property
    def imag(self) -> Real:
        return self.__imag

    @property
    def sin(self) -> Real:
        return self.imag / abs(self)

    @property
    def cos(self) -> Real:
        return self.real / abs(self)

    @property
    def tan(self) -> Real:
        if self.cos == 0:
            return 1e30

        return self.sin / self.cos

    def conjugate(self) -> Complex:
        return self.__class__(self.real, (-self.imag))

    @staticmethod
    def cis(angle: Real, radian=False) -> Complex:
        if radian:
            x = math.cos(angle)
            y = math.sin(angle)
        else:
            radians = angle * math.pi / 180
            x = math.cos(radians)
            y = math.sin(radians)

        return ComplexNumber(x, y)

    def rotate(self, degree: Real, radian=False) -> Complex:
        return self * ComplexNumber.cis(degree, radian)

    def fracpow(self, a: int, b: int) -> Complex:
        return (self ** a) ** (1 / b)

    def all_roots(self, deg: int) -> Complex:
        roots = []
        roots.append(self ** (1 / deg))

        for pos in range(1, deg):
            roots.append(roots[-1].rotate(2*math.pi / deg, radian=True))

        return roots

    def __add__(self, other) -> Complex:
        if isinstance(other, self.__class__):
            return self.__class__((self.real + other.real), (self.imag + other.imag))
        if isinstance(other, Real):
            return self.__class__((self.real + other.real), self.imag)

    def __neg__(self) -> Complex:
        return self.__class__((-self.real), (-self.imag))

    def __pos__(self) -> Complex:
        return self.__class__((+self.real), (+self.imag))

    def __mul__(self, other) -> Complex:
        if isinstance(other, self.__class__):
            real_part = (self.real * other.real - self.imag * other.imag)
            imag_part = (self.real * other.imag + other.real * self.imag)
            return self.__class__(real_part, imag_part)
        if isinstance(other, Real):
            return self.__class__(self.real * other, self.imag * other)

    def __rmul__(self, other) -> Complex:
        return self * other

    def __truediv__(self, other) -> Complex:
        if isinstance(other, Real):
            return self.__class__(self.real / other, self.imag / other)

        return other.__rtruediv__(self)

    def __rtruediv__(self, other) -> Complex:
        if isinstance(other, Real):
            result = self.__class__(other, 0)
        else:
            result = other

        return result * self.conjugate() / (abs(self) ** 2)

    def __pow__(self, power) -> Complex:
        if not power % 1 == 0:
            if (1 / power) % 1 == 0:
                new_angle = math.atan(self.tan) * power
                new_module = abs(self) ** (power)
                return (new_module * ComplexNumber.cis(new_angle, radian=True))

            raise NotImplementedError("If you want to get z ** (a / b) use z.fracpow(a, b)")

        result = 1
        for _ in range(power):
            result *= self
        return result

    def __abs__(self) -> Real:
        return (self.real ** 2 + self.imag ** 2) ** (1 / 2)

    def __eq__(self, other) -> bool:
        if not self.imag:
            return self.real == other
        return self.real == other.real and self.imag == other.imag

    def __rpow__(self, other):
        raise NotImplementedError

    def __radd__(self, other) -> Complex:
        return self + other

    def __bool__(self) -> bool:
        return self.real or self.imag

    def __repr__(self) -> str:
        real = round(self.real, self.precision) if round(self.real, self.precision - 1) % 1 != 0 else round(self.real)
        imag = round(self.imag, self.precision) if round(self.imag, self.precision - 1) % 1 != 0 else round(self.imag)

        if real == 0:
            if imag == 0:
                return '0'
            if imag == 1:
                return 'i'
            elif imag == -1:
                return '-i'
            return f'{imag}i'
        if imag > 0:
            return f'{real} + {imag}i' if imag != 1 else f'{real} + i'
        elif imag < 0:
            return f'{real} - {(-1) * imag}i' if imag != -1 else f'{real} - i'
        elif imag == 0:
            return str(real)

    def __str__(self) -> str:
        return self.__repr__()

    def __complex__(self) -> str:
        return self.__repr__()

    def __hash__(self) -> int:
        return hash(self.real) ^ hash(self.imag)

    def __float__(self) -> Complex:
        return self.__class__(float(self.real), float(self.imag))

    def __int__(self) -> Real:
        return self.__class__(int(self.real), int(self.imag))

    def __round__(self, n=None) -> Complex:
        return self.__class__(round(self.real, n), round(self.imag, n))


def sqrt(number: Complex) -> Complex:
    if isinstance(number, Real):
        number = ComplexNumber(number, 0)
    if abs(number) == 0:
        return 0
    sin_half, cos_half = half_cis(number.sin, number.cos)
    new_abs = abs(number) ** (1 / 2)
    real = new_abs * cos_half
    imag = new_abs * sin_half
    return ComplexNumber(real, imag)


i = ComplexNumber(0, 1)
