from math import *

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

  def __lt__(self, other):
    if self.x == other.x:
      return self.y < other.y
    return self.x < other.x

  def length(self) -> float:
    return sqrt(self.x * self.x + self.y * self.y)

  def normalize(self):
    self_len = self.length()
    self.x /= self_len
    self.y /= self_len

  def multiply(self, scale:float):
    self.x *= scale
    self.y *= scale

  def multiply_copy(self, scale:float):
    result = Point(self.x, self.y)
    result.multiply(scale)
    return result

  def add_copy(self, other):
    return Point(self.x + other.x, self.y + other.y)

  def subtract_floats_copy(self, x:float,  y:float):
    return Point(self.x - x, self.y - y)

  def subtract_copy(self, other):
    return Point(self.x - other.x, self.y - other.y)

  def perpendicular_copy(self):
    length = self.length()
    angle = self.angle()
    return Point( length * cos(angle + pi / 2),
                  length * sin(angle + pi / 2))

  def angle(self) -> float:
    return atan2(self.y, self.x)

  def rotate_copy(self, rads:float):
    ca = cos(rads)
    sa = sin(rads)
    return Point(ca * self.x - sa * self.y,
                 sa * self.x + ca * self.y)


class Line:
  def __init__(self, p1:Point, p2:Point) -> None:
    self.a = (p1.y - p2.y)
    self.b = (p2.x - p1.x)
    self.c = -(p1.x*p2.y - p2.x*p1.y)


class Rect:
  def __init__(self, x:float, y:float, w:float, h:float):
    self.x = x
    self.y = y
    self.w = w
    self.h = h

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

  def contains(self, x:float, y:float) -> bool:
    return x >= self.x and y >= self.y and x <= self.right() and y <= self.bottom()

  def contains_point(self, point:Point) -> bool:
    return self.contains(point.x, point.y)

  def shrink_xy_copy(self, amount_x:float, amount_y:float):
    return Rect(self.x + amount_x, self.y + amount_y, self.w - amount_x * 2, self.h - amount_y * 2)

  def shrink_copy(self, amount:float):
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

