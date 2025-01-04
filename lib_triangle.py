from lib import *

class TriangleOptions:
  triangle_step_size: int
  triangle_angle: float
  triangle_rotate: bool
  triangle_rotate_range: RangeFloat
  triangle_do_shuffle: bool
  triangle_shuffle_range: float


def _create_adjusted_point(
  default:Point,
  params: TriangleOptions
) -> Point:
  shuffle_range = try_get(params, 'triangle_shuffle_range', 0)
  if shuffle_range <= 0:
    return default
  x_range = RangeInt(-shuffle_range, shuffle_range)
  y_range = RangeInt(-shuffle_range, shuffle_range)
  x_delta = x_range.rand()
  y_delta = y_range.rand()
  x = default.x + x_delta
  y = default.y + y_delta
  return Point(x, y)


# TODOML option to use this
def _draw_scaled_triangle(center:Point, corners:List[Point], scale:float, group:Group = None) -> List[Point]:
  result: List[Point] = []
  for corner in corners:
    scaled = corner.subtract_copy(center)
    scaled.multiply(scale)
    scaled = scaled.add_copy(center)
    result.append(scaled)
  # Re-add the first point to close the loop
  result.append(result[0])
  # draw_point_path(result, group)
  return result


def _create_scaled_triangle_loop(center: Point, corners: List[Point], count: int, dist_per: float) -> List[Point]:
  scaled_corners: List[List[Point]] = []

  for i in range(0, count):
    index = count - i
    triangle: List[Point] = []
    scaled_corners.append(triangle)
    for corner in corners:
      scaled = corner.subtract_copy(center).normalize().multiply(dist_per * index).add(center)
      triangle.append(scaled)

  result: List[Point] = []
  for i in range(0, len(scaled_corners) - 1):
    current = scaled_corners[i]
    if i == 0:
      result.append(current[0])
    result.append(current[1])
    result.append(current[2])
    next = scaled_corners[i + 1]

    current_line = Line(current[2], current[0])
    next_line = Line(next[0], next[1])
    intersection = line_intersection(current_line, next_line)
    if intersection is None:
      continue
    result.append(intersection)

  # Add the last ones in too
  final = scaled_corners[-1]
  result.append(final[1])
  result.append(final[2])

  return result

class TriangleResult:
  def __init__(
      self,
      triangle_points: List[Point],
      top: Point,
      left: Point,
      right: Point,
      center: Point
  ):
    self.triangle_points = triangle_points
    self.top = top
    self.left = left
    self.right = right
    self.center = center


def create_triangle_lines(pad_rect: Rect, params: TriangleOptions) -> TriangleResult:
  center = pad_rect.center()
  rot_rad = try_get(params, 'triangle_rotate_range', RangeFloat(0, 180)).rand() * deg_to_rad

  bottom_line = Line(Point(pad_rect.x, pad_rect.bottom()), Point(pad_rect.right(), pad_rect.bottom()))
  rot_angle = try_get(params, 'triangle_angle', 30)

  # Create base points
  top = Point(center.x, pad_rect.y)
  left_line = Line(top, Point(0, 1).rotate(rot_angle * deg_to_rad).add(top))
  right_line = Line(top, Point(0, 1).rotate(-rot_angle * deg_to_rad).add(top))
  left = line_intersection(left_line, bottom_line)
  right = line_intersection(right_line, bottom_line)

  # Rotate points
  if try_get(params, 'triangle_rotate', False):
    top_delta = top.subtract_copy(center)
    top_delta = top_delta.rotate_copy(rot_rad)
    top = center.add_copy(top_delta)
    left_delta = left.subtract_copy(center)
    left_delta = left_delta.rotate_copy(rot_rad)
    left = center.add_copy(left_delta)
    right_delta = right.subtract_copy(center)
    right_delta = right_delta.rotate_copy(rot_rad)
    right = center.add_copy(right_delta)

  # Adjust points
  if try_get(params, 'triangle_do_shuffle', False):
    top = _create_adjusted_point(top, params)
    left = _create_adjusted_point(left, params)
    right = _create_adjusted_point(right, params)

  # Collect final corners, find center
  corners = [top, right, left]
  triangle_center = average_points(corners)

  # Find the shortest distance to center
  min_dist = maxsize
  for corner in corners:
    delta = triangle_center.subtract_copy(corner)
    dist = delta.length()
    min_dist = min(dist, min_dist)

  # Separate into steps
  count = floor(min_dist / params.triangle_step_size)
  dist_per = min_dist / count

  # Create point arrays
  triangle_points = _create_scaled_triangle_loop(triangle_center, corners, count, dist_per)
  return TriangleResult(triangle_points, top, left, right, center)