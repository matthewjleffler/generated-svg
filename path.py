import lib
import math
import random
from typing import List

round_digits = 0 # How many digits to round positions to
size_digits = 2 # How many digits to round the radius size to

class Position:
  def __init__(self, x, y, size) -> None:
    self.x = x
    self.y = y
    self.size = size

  def point(self) -> lib.Point:
    return lib.Point(self.x, self.y)


def subdivide_point_path(rough:List[lib.Point], sub_min:int, sub_max:int) -> List[lib.Point]:
  last = rough[0]
  points: List[lib.Point] = []
  points.append(rough[0])

  for i in range(1, len(rough)):
    point = rough[i]
    vector = point.subtract(last)
    length = vector.length()

    subdivisions = random.randint(sub_min, sub_max)
    if i == 1 or i == len(rough) - 1:
      subdivisions = 1

    sub_length = length / subdivisions
    vector.normalize()
    vector.multiply(sub_length)

    x = last.x
    y = last.y
    lib.add_nondup_point(round(x, 0), round(y, 0), points)
    for _ in range(0, subdivisions):
      x += vector.x
      y += vector.y
      lib.add_nondup_point(round(x, 0), round(y, 0), points)
    last = point

  return points


def clean_duplicates(points:List[lib.Point]):
  i = len(points)
  while i > 1:
    i -= 1
    last = points[i]
    next = points[i - 1]
    if last.x == next.x and last.y == next.y:
      points.pop(i)


def shuffle_points(range_x:float, range_y:float, points:List[lib.Point]):
  for point in points:
    change_x = random.randrange(-range_x, range_x)
    change_y = random.randrange(-range_y, range_y)
    point.x += change_x
    point.y += change_y


def add_nondup_position(x:float, y:float, size:float, array:List[Position]):
  for item in array:
    if item.x == x and item.y == y and item.size == size:
      return
  array.append(Position(x, y, size))


def step_along_quadratic(start:float, end:float, control:lib.Point, t:float) -> lib.Point:
  x = (1 - t) * (1 - t) * start.x + 2 * (1 - t) * t * control.x + t * t * end.x
  y = (1 - t) * (1 - t) * start.y + 2 * (1 - t) * t * control.y + t * t * end.y
  return lib.Point(x, y)


def add_points_along_line(p0:lib.Point, p1:lib.Point, size:float, next_size:float, step_dist:float, positions:List[Position]):
  vector = p1.subtract(p0)
  length = vector.length()
  vector.normalize()

  copy = vector.multiply_copy(step_dist)
  copy_len = copy.length()
  while copy_len < length:
    step_size = round(lib.ease_in_out_quad(copy_len, size, next_size - size, length), size_digits)
    # step_size = round(lib.lerp(size, next_size, copy_len / length), size_digits)

    add_nondup_position(round(p0.x + copy.x, round_digits), round(p0.y + copy.y, round_digits), step_size, positions)
    copy = vector.multiply_copy(copy_len + step_dist)
    copy_len = copy.length()

  add_nondup_position(round(p1.x, round_digits), round(p1.y, round_digits), next_size, positions)


def add_points_along_curve(p0:lib.Point, p1:lib.Point, control:lib.Point, size:float, next_size:float, step_dist:float, positions:List[Position]):
  vector = p1.subtract(p0)
  length = vector.length() * 1.1
  steps = math.floor(length / step_dist)

  for i in range(0, steps):
    t = i / steps
    point = step_along_quadratic(p0, p1, control, t)

    step_size = round(lib.ease_in_out_quad(t, size, next_size - size, 1), size_digits)
    # step_size = lib.lerp(size, next_size, t)

    add_nondup_position(round(point.x, round_digits), round(point.y, round_digits), step_size, positions)

  # Finish with final point
  add_nondup_position(round(p1.x, round_digits), round(p1.y, round_digits), next_size, positions)


def draw_point_circles(points:List[lib.Point]):
  for point in points:
    lib.circ(point.x, point.y, 5)


def draw_point_path(points:List[lib.Point]):
  last = points[0]
  path = "M{} {}".format(last.x, last.y)
  for i in range(1, len(points)):
    point = points[i]
    path += " L{} {}".format(point.x, point.y)
  lib.path(path)


def draw_curved_path(points:List[lib.Point], centers:List[lib.Point]):
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

  lib.path(path)


def generate_centerpoints(points:List[lib.Point]) -> List[lib.Point]:
  centers = []

  # Generate centerpoints
  last = points[0]
  for i in range(1, len(points)):
    point = points[i]

    # Calculuate center point
    vector = point.subtract(last)
    length = vector.length()
    vector.normalize()
    vector.multiply(length / 2)

    center_x = last.x + vector.x
    center_y = last.y + vector.y
    centers.append(lib.Point(center_x, center_y))

    # lib.circ(center_x, center_y, 5)

    last = point

  return centers


def generate_final_positions(points: List[lib.Point], centers: List[lib.Point], size_end:float, size_min:float, size_max:float, step_dist:float) -> List[Position]:
  positions: List[Position] = []

  # Start point
  add_nondup_position(round(points[0].x, round_digits), round(points[0].y, 0), size_end, positions)
  size = size_end
  next_size = 0

  # Add positions
  for i in range(1, len(points) + 1):
    next_size = random.randrange(size_min, size_max)
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

