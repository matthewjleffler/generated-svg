from lib import *
from math import *
from typing import List


###
### Path Drawing
###


_round_digits = 0 # How many digits to round positions to
_size_digits = 2 # How many digits to round the radius size to

class Position:
  def __init__(self, x, y, size) -> None:
    self.x = x
    self.y = y
    self.size = size

  def point(self) -> Point:
    return Point(self.x, self.y)

def offest_point_path(original:List[Point], offset:Point) -> List[Point]:
  result: List[Point] = []
  for val in original:
    result.append(Point(val.x + offset.x, val.y + offset.y))
  return result

def subdivide_point_path(rough:List[Point], sub_count:RangeInt, ignored_indexes: List[int] = []) -> List[Point]:
  last = rough[0]
  points: List[Point] = []
  points.append(rough[0])

  for i in range(1, len(rough)):
    point = rough[i]
    vector = point.subtract_copy(last)
    length = vector.length()

    subdivisions = sub_count.rand()
    if i in ignored_indexes:
      subdivisions = 1

    sub_length = length / subdivisions
    vector.normalize()
    vector.multiply(sub_length)

    x = last.x
    y = last.y
    for _ in range(0, subdivisions):
      x += vector.x
      y += vector.y
      add_nondup_floats(x, y, points)
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
    change_x = rand_float(-range_x, range_x)
    change_y = rand_float(-range_y, range_y)
    point.x += change_x
    point.y += change_y


def add_nondup_position(x:float, y:float, size:float, array:List[Position]):
  x = round(x, _round_digits)
  y = round(y, _round_digits)
  size = round(size, _size_digits)
  for item in array:
    if item.x == x and item.y == y and item.size == size:
      return
  array.append(Position(x, y, size))


def _step_along_quadratic(start:float, end:float, control:Point, t:float) -> Point:
  x = (1 - t) * (1 - t) * start.x + 2 * (1 - t) * t * control.x + t * t * end.x
  y = (1 - t) * (1 - t) * start.y + 2 * (1 - t) * t * control.y + t * t * end.y
  return Point(x, y)


def _add_points_along_line(p0:Point, p1:Point, size:float, next_size:float, step_dist:float, positions:List[Position]):
  vector = p1.subtract_copy(p0)
  length = vector.length()
  vector.normalize()

  copy = vector.multiply_copy(step_dist)
  copy_len = copy.length()
  while copy_len < length:
    step_size = ease_in_out_quad(copy_len, size, next_size - size, length)
    # step_size = lerp(size, next_size, copy_len / length)

    add_nondup_position(p0.x + copy.x, p0.y + copy.y, step_size, positions)
    copy = vector.multiply_copy(copy_len + step_dist)
    copy_len = copy.length()

  add_nondup_position(p1.x, p1.y, next_size, positions)

def bezier_length_simple(p0:Point, p1:Point, control:Point) -> float:
  vector = p1.subtract_copy(control)
  length = vector.length()
  vector = control.subtract_copy(p0)
  length += vector.length()
  return length

def bezier_length_fine(p0:Point, p1:Point, control:Point) -> float:
  length = 0
  last = p0
  subd = 10
  for i in range(1, subd + 1):
    t = i / subd
    point = _step_along_quadratic(p0, p1, control, t)
    delta = point.subtract_copy(last)
    length += delta.length()
    last = point
  return length

def subdivide_quadratic(p0:Point, p1:Point, control:Point, step_dist:float, result:List[Point]):
  length = bezier_length_fine(p0, p1, control)
  steps = floor(length / step_dist)

  for i in range(0, steps + 1):
    t = i / steps
    point = _step_along_quadratic(p0, p1, control, t)
    result.append(point)

  clean_duplicates(result)


def _add_points_along_curve(p0:Point, p1:Point, control:Point, size:float, next_size:float, step_dist:float, positions:List[Position]):
  # Calculate rough distance
  length = bezier_length_simple(p0, p1, control)
  steps = floor(length / step_dist)

  for i in range(0, steps):
    t = i / steps
    point = _step_along_quadratic(p0, p1, control, t)

    step_size = ease_in_out_quad(t, size, next_size - size, 1)
    # step_size = lerp(size, next_size, t)

    add_nondup_position(point.x, point.y, step_size, positions)

  # Finish with final point
  add_nondup_position(p1.x, p1.y, next_size, positions)


def draw_point_circles(points:List[Point], group:Group = None):
  for point in points:
    draw_circ(point.x, point.y, 5, group)


class HatchParams:
  def __init__(self, on_range:RangeInt, off_range:RangeInt) -> None:
    self.on_range = on_range
    self.off_range = off_range

  def on(self) -> float:
    return self.on_range.rand()

  def off(self) -> float:
    return self.off_range.rand()


class HatchState:
  def __init__(self) -> None:
    self.current = 0
    self.on = True

  def set_on_state(self, on:bool, params:HatchParams):
    self.on = on
    if on:
      self.current = params.on_range.rand()
    else:
      self.current = params.off_range.rand()

def draw_point_path_hatched(points:List[Point], params:HatchParams, group:Group = None):
  hatch = HatchState()
  hatch.set_on_state(True, params)

  last = points[0]
  last_m = Point(last.x, last.y)
  path = ""
  for i in range(1, len(points)):
    next = points[i]
    delta = next.subtract_copy(last)
    segment_len = delta.length()
    delta.normalize()
    current_point = last.copy()

    while segment_len > 0:
      step_len = min(segment_len, hatch.current)

      change_point = delta.multiply_copy(step_len)
      current_point = current_point.add_copy(change_point)

      if hatch.on:
        if last_m is not None:
          path += f"M{round(last_m.x, _size_digits)} {round(last_m.y, _size_digits)}"
          last_m = None
        path += f"L{round(current_point.x, _size_digits)} {round(current_point.y, _size_digits)}"
      else:
        last_m = Point(current_point.x, current_point.y)

      segment_len -= step_len
      hatch.current -= step_len
      if hatch.current <= 0:
        hatch.set_on_state(not hatch.on, params)

    last = next
  draw_path(path, group)

def draw_point_path(points:List[Point], group:Group = None):
  last = points[0]
  path = "M{} {}".format(last.x, last.y)
  for i in range(1, len(points)):
    point = points[i]
    path += " L{} {}".format(point.x, point.y)
  draw_path(path, group)


def draw_curved_path(points:List[Point], centers:List[Point], group:Group = None):
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

  draw_path(path, group)


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

    # draw_circ(center_x, center_y, 5, group)

    last = point

  return centers


def generate_final_positions(points: List[Point], centers: List[Point], size_end:float, size_range:RangeInt, step_dist:float) -> List[Position]:
  positions: List[Position] = []

  # Start point
  add_nondup_position(points[0].x, points[0].y, size_end, positions)
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
      _add_points_along_line(p0, p1, size, next_size, step_dist, positions)
    elif i == len(points):
      # Draw straight line at end
      p0 = centers[i - 2]
      p1 = points[i - 1]
      _add_points_along_line(p0, p1, size, next_size, step_dist, positions)
    else:
      # Draw along quadratic bezier curve for each other step
      p0 = centers[i - 2]
      p1 = centers[i - 1]
      control = points[i - 1]
      _add_points_along_curve(p0, p1, control, size, next_size, step_dist, positions)

    size = next_size

  return positions

