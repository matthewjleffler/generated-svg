from lib import *
from lib_path import *


###
### Triangle Design
###

class TriangleParams:
  def __init__(self) -> None:
    self.draw_triangles = True
    self.pad = 0
    self.point_range = 100
    self.step_size = 5
    self.rotate_range = RangeFloat(0, 180)


def _create_adjusted_point(
  pad_rect:Rect,
  default:Point,
  params:TriangleParams
) -> Point:
  x_range = RangeInt(-params.point_range, params.point_range)
  y_range = RangeInt(-params.point_range, params.point_range)
  x_delta = x_range.rand()
  y_delta = y_range.rand()
  x = default.x + x_delta
  y = default.y + y_delta
  x = clamp(x, pad_rect.x, pad_rect.right())
  y = clamp(y, pad_rect.y, pad_rect.bottom())
  return Point(x, y)


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


def average_point(points:List[Point]) -> Point:
  count = len(points)
  if count < 1:
    return Point(0,0)
  sum_x = 0
  sum_y = 0
  for point in points:
    sum_x += point.x
    sum_y += point.y
  return Point(sum_x / count, sum_y / count)


def draw_triangle(params:TriangleParams, group:Group = None):
  # draw_border(group)

  pad_rect = svg_safe().shrink_copy(params.pad)
  # Draw pad rect
  # draw_rect(pad_rect.x, pad_rect.y, pad_rect.w, pad_rect.h, group)

  center = Point(pad_rect.center_x(), pad_rect.center_y())
  half_x = pad_rect.w / 2
  half_y = pad_rect.h / 2
  rot_rad = params.rotate_range.rand() * deg_to_rad

  # Create base points
  top = Point(center.x, center.y - half_y)
  left = Point(center.x - half_x, center.y + half_y)
  right = Point(center.x + half_x, center.y + half_y)

  # Rotate points
  top_delta = top.subtract_copy(center)
  top_delta = top_delta.rotate_copy(rot_rad)
  top = center.add_copy(top_delta)
  left_delta = left.subtract_copy(center)
  left_delta = left_delta.rotate_copy(rot_rad)
  left = center.add_copy(left_delta)
  right_delta = right.subtract_copy(center)
  right_delta = right_delta.rotate_copy(rot_rad)
  right = center.add_copy(right_delta)

  # Adjust points and clamp to pad
  top = _create_adjusted_point(pad_rect, top, params)
  left = _create_adjusted_point(pad_rect, left, params)
  right = _create_adjusted_point(pad_rect, right, params)

  # Collect final corners, find center
  corners = [top, right, left]
  center = average_point(corners)

  # Find the shortest distance to center
  min_dist = maxsize
  for corner in corners:
    delta = center.subtract_copy(corner)
    dist = delta.length()
    min_dist = min(dist, min_dist)

  # Separate into steps
  count = floor(min_dist / params.step_size)

  # Create point arrays
  all_points: List[List[Point]] = []
  for i in range(0, count):
    scale = 1 - (i / count)
    points = _draw_scaled_triangle(center, corners, scale)
    all_points.append(points)

  # Draw points
  if params.draw_triangles:
    # hatch_params = HatchParams(10, 5)
    hatch_params = HatchParams(RangeInt(10, 30), RangeInt(2, 2))

    for points in all_points:
      # draw_point_path(points, group)
      draw_point_path_hatched(points, hatch_params, group)

