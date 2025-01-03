from math import *
from lib_rand import *
from typing import List

###
### Math Helpers
###

### Constants
deg_to_rad = pi / 180


class Point:
  def __init__(self, x:float, y:float):
    self.x = x
    self.y = y

  def __repr__(self) -> str:
    return f"[Point] x:{self.x} y:{self.y}"

  def __lt__(self, other: 'Point') -> bool:
    if self.x == other.x:
      return self.y < other.y
    return self.x < other.x

  def length(self) -> float:
    return sqrt(self.x * self.x + self.y * self.y)

  def normalize(self) -> 'Point':
    self_len = self.length()
    if self_len <= 0:
      return Point(0, 0)
    self.x /= self_len
    self.y /= self_len
    return self

  def copy(self) -> 'Point':
    return Point(self.x, self.y)

  def divide(self, scale:float) -> 'Point':
    self.x /= scale
    self.y /= scale
    return self

  def multiply(self, scale:float) -> 'Point':
    self.x *= scale
    self.y *= scale
    return self

  def multiply_copy(self, scale:float) -> 'Point':
    result = Point(self.x, self.y)
    result.multiply(scale)
    return result

  def multiply_floats(self, scale_x: float, scale_y: float) -> 'Point':
    self.x *= scale_x
    self.y *= scale_y
    return self

  def multiply_point(self, other: 'Point') -> 'Point':
    return self.multiply_floats(other.x, other.y)

  def add(self, other: 'Point') -> 'Point':
    return self.add_floats(other.x, other.y)

  def add_floats(self, x: float, y: float) -> 'Point':
    self.x += x
    self.y += y
    return self

  def add_copy(self, other: 'Point') -> 'Point':
    return Point(self.x + other.x, self.y + other.y)

  def add_floats_copy(self, x: float, y: float) -> 'Point':
    return Point(self.x + x, self.y + y)

  def subtract(self, other: 'Point') -> 'Point':
    self.x -= other.x
    self.y -= other.y
    return self

  def subtract_floats(self, x: float, y: float) -> 'Point':
    self.x -= x
    self.y -= y
    return self

  def subtract_floats_copy(self, x:float,  y:float) -> 'Point':
    return Point(self.x - x, self.y - y)

  def subtract_copy(self, other: 'Point') -> 'Point':
    return Point(self.x - other.x, self.y - other.y)

  def perpendicular_copy(self) -> 'Point':
    length = self.length()
    angle = self.angle()
    return Point( length * cos(angle + pi / 2),
                  length * sin(angle + pi / 2))

  def angle(self) -> float:
    return atan2(self.y, self.x)

  def rotate(self, rads:float) -> 'Point':
    ca = cos(rads)
    sa = sin(rads)
    tx = ca * self.x - sa * self.y
    ty = sa * self.x + ca * self.y
    self.x = tx
    self.y = ty
    return self

  def rotate_copy(self, rads:float) -> 'Point':
    ca = cos(rads)
    sa = sin(rads)
    return Point(ca * self.x - sa * self.y,
                 sa * self.x + ca * self.y)

  def dot(self, other: 'Point') -> float:
    return self.x * other.x + self.y * other.y

  def clamp(self, rect: 'Rect') -> 'Point':
    if self.x < rect.x:
      self.x = rect.x
    if self.x > rect.right():
      self.x = rect.right()
    if self.y < rect.y:
      self.y = rect.y
    if self.y > rect.bottom():
      self.y = rect.bottom()
    return self

  def to_int(self) -> tuple[int, int]:
    return (floor(self.x), floor(self.y))


class Line:
  def __init__(self, p0:Point, p1:Point) -> None:
    self.p0 = p0.copy()
    self.p1 = p1.copy()
    self.a = (p0.y - p1.y)
    self.b = (p1.x - p0.x)
    self.c = -(p0.x*p1.y - p1.x*p0.y)

  def __repr__(self) -> str:
    return f"[Line] x0:{self.p0.x} y0:{self.p0.y} x1:{self.p1.x} y1:{self.p1.y}"

  def normal(self) -> Point:
    dx = self.p1.x - self.p0.x
    dy = self.p1.y - self.p0.y
    return Point(-dy, dx).normalize()

  def normal2(self) -> Point:
    dx = self.p1.x - self.p0.x
    dy = self.p1.y - self.p0.y
    return Point(dy, -dx).normalize()

  def points(self) -> List[Point]:
    return [self.p0, self.p1]

  def vec(self) -> Point:
    return self.p1.subtract_copy(self.p0).normalize()

  def length(self) -> float:
    return self.p1.subtract_copy(self.p0).length()

  def dot(self, other: 'Line') -> float:
    return self.vec().dot(other.vec())

  def add(self, delta: Point) -> 'Line':
    self.p0.add(delta)
    self.p1.add(delta)
    return self

  def multiply(self, scale: Point) -> 'Line':
    self.p0.x *= scale.x
    self.p1.x *= scale.x
    self.p0.y *= scale.y
    self.p1.y *= scale.y
    return self

  def reverse(self) -> 'Line':
    t0 = self.p0
    self.p0 = self.p1
    self.p1 = t0
    return self


class ExpandingVolume:
  def __init__(self, list: List[Point] = None):
    self.min_x = float('inf')
    self.min_y = float('inf')
    self.max_x = float('-inf')
    self.max_y = float('-inf')

    if list is not None:
      for point in list:
        self.add(point)

  def add(self, point: Point):
    self.min_x = min(point.x, self.min_x)
    self.min_y = min(point.y, self.min_y)
    self.max_x = max(point.x, self.max_x)
    self.max_y = max(point.y, self.max_y)

  def add_list(self, points: List[Point]):
    for point in points:
      self.add(point)

  def add_lists(self, point_list: List[List[Point]]):
    for points in point_list:
      self.add_list(points)

  def to_rect(self) -> 'Rect':
    return Rect.from_edges(self.min_x, self.min_y, self.max_x, self.max_y)


class Rect:
  def __init__(self, x:float, y:float, w:float, h:float):
    self.x = x
    self.y = y
    self.w = w
    self.h = h
    self.range_x = RangeInt(self.x, self.x + self.w)
    self.range_y = RangeInt(self.y, self.y + self.h)

  @staticmethod
  def from_edges(x: float, y: float, r: float, b: float) -> 'Rect':
    w = r - x
    h = b - y
    return Rect(x, y, w, h)

  def __repr__(self) -> str:
    return f"[Rect] x:{self.x} y:{self.y} w:{self.w} h:{self.h} cx:{self.center_x()} cy:{self.center_y()} r:{self.right()} b:{self.bottom()}"

  def bottom(self) -> float:
    return self.y + self.h

  def right(self) -> float:
    return self.x + self.w

  def center_x(self) -> float:
    return floor(self.x + self.w / 2)

  def center_y(self) -> float:
    return floor(self.y + self.h / 2)

  def center(self) -> Point:
    return Point(self.x + self.w / 2, self.y + self.h / 2)

  def contains(self, x:float, y:float) -> bool:
    return x >= self.x and y >= self.y and x <= self.right() and y <= self.bottom()

  def contains_point(self, point:Point) -> bool:
    return self.contains(point.x, point.y)

  def copy(self) -> 'Rect':
    return Rect(self.x, self.y, self.w, self.h)

  def shrink_xy_copy(self, amount_x:float, amount_y:float) -> 'Rect':
    return Rect(self.x + amount_x, self.y + amount_y, self.w - amount_x * 2, self.h - amount_y * 2)

  def shrink_copy(self, amount:float) -> 'Rect':
    return Rect(self.x + amount, self.y + amount, self.w - amount * 2, self.h - amount * 2)


# Helper Functions
def lerp(a:float, b:float, t:float) -> float:
  return round((1 - t) * a + t * b, 2)

def ease_in_out_quad(t:float, b:float, c:float, d:float) -> float:
  return round(-c / 2 * (cos(pi * t / d) - 1) + b, 2)

def line_intersection(L1:Line, L2:Line) -> Point:
  D  = L1.a * L2.b - L1.b * L2.a
  Dx = L1.c * L2.b - L1.b * L2.c
  Dy = L1.a * L2.c - L1.c * L2.a
  if D != 0:
    x = Dx / D
    y = Dy / D
    return Point(x, y)
  else:
    return None

def scale_rect_to_fit(full: Rect, target: Rect) -> tuple[Point, float]:
  scale_x = target.w / full.w
  scale_y = target.h / full.h
  final_scale = min(scale_x, scale_y)

  final_w = full.w * final_scale
  final_h = full.h * final_scale
  offset_x = (target.x - (full.x * final_scale) + (target.w - final_w) / 2)
  offset_y = (target.y - (full.y * final_scale) + (target.h - final_h) / 2)
  return (Point(offset_x, offset_y), final_scale)
