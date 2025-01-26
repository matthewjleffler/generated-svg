from math import *
from .lib_math import *
from typing import List
from sys import float_info


### Matrix Math
### Based on logic from: https://github.com/leeoniya/transformation-matrix-js/blob/master/src/matrix.js

def __is_equal(a: float, b: float) -> bool:
  return abs(a - b) < float_info.epsilon

class Matrix:
  def __init__(self):
    ## Scale X
    self._a: float = 1
    ## Skew Y
    self._b: float = 0
    ## Skew X
    self._c: float = 0
    ## Scale Y
    self._d: float = 1
    ## Translate X
    self._e: float = 0
    ## Translate Y
    self._f: float = 0

  def __repr__(self) -> str:
    return f"[Matrix] x:{self.get_x()} y:{self.get_y()} scale_x: {self.get_scale_x()} scale_y: {self.get_scale_y()}, skewx: {self.get_skew_x()} skewy: {self.get_skew_y()}"

  def get_scale_x(self) -> float:
    return self._a

  def get_scale_y(self) -> float:
    return self._d

  def get_x(self) -> float:
    return self._e

  def get_y(self) -> float:
    return self._f

  def get_skew_x(self) -> float:
    return self._c

  def get_skew_y(self) -> float:
    return self._b

  # TODOML rot?

  def __set(self, a: float, b: float, c: float, d: float, e: float, f: float) -> 'Matrix':
    self._a = a
    self._b = b
    self._c = c
    self._d = d
    self._e = e
    self._f = f
    return self

  def __transform(self, a2: float, b2: float, c2: float, d2: float, e2: float, f2: float) -> 'Matrix':
    a1 = self._a
    b1 = self._b
    c1 = self._c
    d1 = self._d
    e1 = self._e
    f1 = self._f

    # Matrix order:
    #  ace
    #  bdf
    #  001
    return self.__set(
      a1 * a2 + c1 * b2,
      b1 * a2 + d1 * b2,
      a1 * c2 + c1 * d2,
      b1 * c2 + d1 * d2,
      a1 * e2 + c1 * f2 + e1,
      b1 * e2 + d1 * f2 + f1
    )

  def flip_x(self) -> 'Matrix':
    return self.__transform(-1, 0, 0, 1, 0, 0)

  def flip_y(self) -> 'Matrix':
    return self.__transform(1, 0, 0, -1, 0, 0)

  # Reset to identity matrix
  def reset(self) -> 'Matrix':
    self._a = self._d = 1
    self._b = self._c = self._e = self._f = 0
    return self

  def rotate(self, rad: float) -> 'Matrix':
    rad_cos = cos(rad)
    rad_sin = sin(rad)
    return self.__transform(rad_cos, rad_sin, -rad_sin, rad_cos, 0, 0)

  def rotate_degree(self, deg: float) -> 'Matrix':
    return self.rotate(deg * deg_to_rad)

  def scale(self, sx: float, sy: float) -> 'Matrix':
    return self.__transform(sx, 0, 0, sy, 0, 0)

  def scale_x(self, sx: float) -> 'Matrix':
    return self.__transform(sx, 0, 0, 1, 0, 0)

  def scale_y(self, sy: float) -> 'Matrix':
    return self.__transform(1, 0, 0, sy, 0, 0)

  def skew(self, sx: float, sy: float) -> 'Matrix':
    return self.__transform(1, sy, sx, 1, 0, 0)

  def skew_x(self, sx: float) -> 'Matrix':
    return self.__transform(1, 0, sx, 1, 0, 0)

  def skew_y(self, sy: float) -> 'Matrix':
    return self.__transform(1, sy, 0, 1, 0, 0)

  def set_to(self, other: 'Matrix') -> 'Matrix':
    return self.__set(other._a, other._b, other._c, other._d, other._e, other._f)

  def translate(self, tx: float, ty: float) -> 'Matrix':
    return self.__transform(1, 0, 0, 1, tx, ty)

  def translate_x(self, tx: float) -> 'Matrix':
    return self.__transform(1, 0, 0, 1, tx, 0)

  def translate_y(self, ty: float) -> 'Matrix':
    return self.__transform(1, 0, 0, 1, 0, ty)

  def translate_point(self, point: Point) -> 'Matrix':
    return self.translate(point.x, point.y)

  def copy(self) -> 'Matrix':
    return Matrix().set_to(self)

  def multiply(self, other: 'Matrix') -> 'Matrix':
    return self.__transform(other._a, other._b, other._c, other._d, other._e, other._f)

  def copy_inverse(self) -> 'Matrix':
    a = self._a
    b = self._b
    c = self._c
    d = self._d
    e = self._e
    f = self._f
    dt = (a * d - b * c)

    return Matrix().__set(
      d / dt,
      -b / dt,
      -c / dt,
      a / dt,
      (c * f - d * e) / dt,
      -(a * f - b * e) / dt
    )

  def copy_interpolated(self, other: 'Matrix', t: float) -> 'Matrix':
    return Matrix().__set(
      self._a + (other._a - self._a) * t,
      self._b + (other._b - self._b) * t,
      self._c + (other._c - self._c) * t,
      self._d + (other._d - self._d) * t,
      self._e + (other._e - self._e) * t,
      self._f + (other._f - self._f) * t
    )

  def apply_to_floats(self, x_y: tuple[float, float]) -> tuple[float, float]:
    (x, y) = x_y
    return (
      x * self._a + y * self._c + self._e,
      x * self._b + y * self._d + self._f
    )

  def apply_to_point(self, point: Point) -> Point:
    (x, y) = self.apply_to_floats((point.x, point.y))
    return Point(x, y)

  def apply_to_point_array(self, points: List[Point]) -> List[Point]:
    result: List[Point] = []
    for point in points:
      result.append(self.apply_to_point(point))
    return result

  def apply_to_point_arrays(self, points: List[List[Point]]) -> List[List[Point]]:
    result: List[List[Point]] = []
    for list in points:
      result.append(self.apply_to_point_array(list))
    return result

  def is_equal(self, other: 'Matrix') -> bool:
    return (
      __is_equal(self._a, other._a) and
      __is_equal(self._b, other._b) and
      __is_equal(self._c, other._c) and
      __is_equal(self._d, other._d) and
      __is_equal(self._e, other._e) and
      __is_equal(self._f, other._f)
    )

  def is_identity(self) -> bool:
    return self.is_equal(Matrix())
