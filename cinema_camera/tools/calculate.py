from __future__ import annotations


import ba

from typing import Union


class Array:
    """Array class to simplify math operations.

    It's better to use numpy here,
    but unfortunately it can't be imported into BombSquad.
    """

    def __init__(self, value: list) -> None:
        self.x: list = value

    def __mul__(self, other: Union[Array, list, float, int]) -> Array:
        if isinstance(other, Array):
            assert len(other.x) == len(self.x)
            return Array([x * other.x[i] for i, x in enumerate(self.x)])

        elif isinstance(other, list):
            assert len(other) == len(self.x)
            return Array([x * other[i] for i, x in enumerate(self.x)])

        elif isinstance(other, (float, int)):
            return Array([x * other for x in self.x])

    def __truediv__(self, other: Union[Array, list, float, int]) -> Array:
        if isinstance(other, Array):
            assert len(other.x) == len(self.x)
            return Array([x / other.x[i] for i, x in enumerate(self.x)])

        elif isinstance(other, list):
            assert len(other) == len(self.x)
            return Array([x / other[i] for i, x in enumerate(self.x)])

        elif isinstance(other, (float, int)):
            return Array([x / other for x in self.x])

    def __add__(self, other: Union[Array, list, float, int]) -> Array:
        if isinstance(other, Array):
            assert len(other.x) == len(self.x)
            return Array([x + other.x[i] for i, x in enumerate(self.x)])

        elif isinstance(other, list):
            assert len(other) == len(self.x)
            return Array([x + other[i] for i, x in enumerate(self.x)])

        elif isinstance(other, (float, int)):
            return Array([x + other for x in self.x])

    def __sub__(self, other: Union[Array, list, float, int]) -> Array:
        if isinstance(other, Array):
            assert len(other.x) == len(self.x)
            return Array([x - other.x[i] for i, x in enumerate(self.x)])

        elif isinstance(other, list):
            assert len(other) == len(self.x)
            return Array([x - other[i] for i, x in enumerate(self.x)])

        elif isinstance(other, (float, int)):
            return Array([x - other for x in self.x])

    def __getitem__(self, key) -> Array:
        val = self.x[key]
        if isinstance(val, list):
            return Array(val)
        return val

    def __setitem__(self, key, value):
        self.x[key] = value

    def __str__(self):
        return f'Array({self.x})'

    def __repr__(self):
        return f'{self.x}'


def try_calculate(function: callable, default_value: float = 0.0) -> any:

    def decorator(x: float):
        try:
            return function(x)
        except:
            return default_value

    return decorator


# def _poly_newton_coefficient(x: list, y: list) -> list:
#     """
#     x: list or np array contanining x data points
#     y: list or np array contanining y data points
#     """
#
#     m = len(x)
#
#     x = np.copy(x)
#     a = np.copy(y)
#     for k in range(1, m):
#         a[k:m] = (a[k:m] - a[k - 1])/(x[k:m] - x[k - 1])
#
#     return a
#
#
# def newton_polynomial(x_data: list, y_data: list) -> callable:
#     """
#     x_data: data points at x
#     y_data: data points at y
#     x: evaluation point(s)
#     """
#     a = _poly_newton_coefficient(x_data, y_data)
#     n = len(x_data) - 1  # Degree of polynomial
#
#     def result(x: float) -> float:
#         p = a[n]
#         for k in range(1, n + 1):
#             p = a[n - k] + (x - x_data[n - k])*p
#
#         return p
#
#     return result


def _poly_newton_coefficient(t: list, x: list, y: list, z: list) -> list:
    """
    x: list or np array contanining x data points
    y: list or np array contanining y data points
    """

    m = len(t)

    t = Array(t)

    x = Array(x)
    y = Array(y)
    z = Array(z)

    for k in range(1, m):
        x[k:m] = (x[k:m] - x[k - 1])/(t[k:m] - t[k - 1])

    for k in range(1, m):
        y[k:m] = (y[k:m] - y[k - 1])/(t[k:m] - t[k - 1])

    for k in range(1, m):
        z[k:m] = (z[k:m] - z[k - 1])/(t[k:m] - t[k - 1])

    return [x, y, z]


def newton_polynomial(time_data: list, x_data: list, y_data: list, z_data: list) -> callable:
    """
    x_data: data points at x
    y_data: data points at y
    x: evaluation point(s)
    """
    a_list = _poly_newton_coefficient(time_data, x_data, y_data, z_data)
    n = len(time_data) - 1  # Degree of polynomial

    def result(t: float) -> ba.Vec3:
        res = []
        for a in a_list:
            p = float(a[n])
            for k in range(1, n + 1):
                p_old = p
                p = a[n - k] + (t - time_data[n - k])*p
            res.append(p)

        return ba.Vec3(res)

    return result
