from lib import *
from math import *
from typing import List

# Path Drawing


_round_digits = 0 # How many digits to round positions to
_size_digits = 2 # How many digits to round the radius size to

class Position:
  def __init__(self, x, y, size) -> None:
    self.x = x
    self.y = y
    self.size = size

  def point(self) -> Point:
    return Point(self.x, self.y)


def subdivide_point_path(rough:List[Point], sub_count:RangeInt, ignore_ends:bool = True) -> List[Point]:
  last = rough[0]
  points: List[Point] = []
  points.append(rough[0])

  for i in range(1, len(rough)):
    point = rough[i]
    vector = point.subtract_copy(last)
    length = vector.length()

    subdivisions = sub_count.rand()
    if ignore_ends:
      if i == 1 or i == len(rough) - 1:
        subdivisions = 1

    sub_length = length / subdivisions
    vector.normalize()
    vector.multiply(sub_length)

    x = last.x
    y = last.y
    # add_nondup_point(round(x, 0), round(y, 0), points)
    for _ in range(0, subdivisions):
      x += vector.x
      y += vector.y
      add_nondup_point(round(x, 0), round(y, 0), points)
    last = point

  return points


def clean_duplicates(points:List[Point]):
  i = len(points)
  while i > 1:
    i -= 1
    last = points[i]
    next = points[i - 1]
    if last.x == next.x and last.y == next.y:
      points.pop(i)


def shuffle_points(range_x:float, range_y:float, points:List[Point]):
  for point in points:
    change_x = rand_int(-range_x, range_x)
    change_y = rand_int(-range_y, range_y)
    point.x += change_x
    point.y += change_y


def add_nondup_position(x:float, y:float, size:float, array:List[Position]):
  for item in array:
    if item.x == x and item.y == y and item.size == size:
      return
  array.append(Position(x, y, size))


def step_along_quadratic(start:float, end:float, control:Point, t:float) -> Point:
  x = (1 - t) * (1 - t) * start.x + 2 * (1 - t) * t * control.x + t * t * end.x
  y = (1 - t) * (1 - t) * start.y + 2 * (1 - t) * t * control.y + t * t * end.y
  return Point(x, y)


def add_points_along_line(p0:Point, p1:Point, size:float, next_size:float, step_dist:float, positions:List[Position]):
  vector = p1.subtract_copy(p0)
  length = vector.length()
  vector.normalize()

  copy = vector.multiply_copy(step_dist)
  copy_len = copy.length()
  while copy_len < length:
    step_size = round(ease_in_out_quad(copy_len, size, next_size - size, length), _size_digits)
    # step_size = round(lerp(size, next_size, copy_len / length), _size_digits)

    add_nondup_position(round(p0.x + copy.x, _round_digits), round(p0.y + copy.y, _round_digits), step_size, positions)
    copy = vector.multiply_copy(copy_len + step_dist)
    copy_len = copy.length()

  add_nondup_position(round(p1.x, _round_digits), round(p1.y, _round_digits), next_size, positions)


def add_points_along_curve(p0:Point, p1:Point, control:Point, size:float, next_size:float, step_dist:float, positions:List[Position]):
  vector = p1.subtract_copy(p0)
  length = vector.length() * 1.1
  steps = floor(length / step_dist)

  for i in range(0, steps):
    t = i / steps
    point = step_along_quadratic(p0, p1, control, t)

    step_size = round(ease_in_out_quad(t, size, next_size - size, 1), _size_digits)
    # step_size = lerp(size, next_size, t)

    add_nondup_position(round(point.x, _round_digits), round(point.y, _round_digits), step_size, positions)

  # Finish with final point
  add_nondup_position(round(p1.x, _round_digits), round(p1.y, _round_digits), next_size, positions)


def draw_point_circles(points:List[Point]):
  for point in points:
    draw_circ(point.x, point.y, 5)


def draw_point_path(points:List[Point]):
  last = points[0]
  path = "M{} {}".format(last.x, last.y)
  for i in range(1, len(points)):
    point = points[i]
    path += " L{} {}".format(point.x, point.y)
  draw_path(path)


def draw_curved_path(points:List[Point], centers:List[Point]):
  point = centers[0]
  path = "M{} {} L{} {}".format(points[0].x, points[0].y, point.x, point.y)

  for i in range(1, len(centers)):
    if i == len(points) -1:
      break
    point = centers[i]
    control = points[i]
    path += " Q{} {} {} {}".format(control.x, control.y, point.x, point.y)

  final = points[len(points) - 1]
  path += " L{} {}".format(final.x, final.y)

  draw_path(path)


def generate_centerpoints(points:List[Point]) -> List[Point]:
  centers = []

  # Generate centerpoints
  last = points[0]
  for i in range(1, len(points)):
    point = points[i]

    # Calculuate center point
    vector = point.subtract_copy(last)
    length = vector.length()
    vector.normalize()
    vector.multiply(length / 2)

    center_x = last.x + vector.x
    center_y = last.y + vector.y
    centers.append(Point(center_x, center_y))

    # circ(center_x, center_y, 5)

    last = point

  return centers


def generate_final_positions(points: List[Point], centers: List[Point], size_end:float, size_range:RangeInt, step_dist:float) -> List[Position]:
  positions: List[Position] = []

  # Start point
  add_nondup_position(round(points[0].x, _round_digits), round(points[0].y, 0), size_end, positions)
  size = size_end
  next_size = 0

  # Add positions
  for i in range(1, len(points) + 1):
    next_size = size_range.rand()
    if i == len(points):
      next_size = size_end

    if i == 1:
      # Draw straight line in beginning
      p0 = points[i - 1]
      p1 = centers[i - 1]
      add_points_along_line(p0, p1, size, next_size, step_dist, positions)
    elif i == len(points):
      # Draw straight line at end
      p0 = centers[i - 2]
      p1 = points[i - 1]
      add_points_along_line(p0, p1, size, next_size, step_dist, positions)
    else:
      # Draw along quadratic bezier curve for each other step
      p0 = centers[i - 2]
      p1 = centers[i - 1]
      control = points[i - 1]
      add_points_along_curve(p0, p1, control, size, next_size, step_dist, positions)

    size = next_size

  return positions

