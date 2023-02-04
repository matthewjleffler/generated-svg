from lib import *
from lib_path import *


###
### Triangle Design
###

class TriangleParams:
  def __init__(self) -> None:
    self.draw_triangles = True
    self.pad = 0
    self.top_range_x = 300
    self.top_range_y = 100
    self.side_range_x = 300
    self.side_range_y = 200
    self.shrink_amt = 20
    self.rotate_range = RangeFloat(0, 180)


def create_adjusted_point(
  pad_rect:Rect,
  default:Point,
  range_x:float,
  range_y:float
) -> Point:
  x_range = RangeInt(-range_x, range_x)
  y_range = RangeInt(-range_y, range_y)
  x_delta = x_range.rand()
  y_delta = y_range.rand()
  x = default.x + x_delta
  y = default.y + y_delta
  x = clamp(x, pad_rect.x, pad_rect.right())
  y = clamp(y, pad_rect.y, pad_rect.bottom())
  return Point(x, y)


def shrink_vec(point:Point, origin:Point, amt:float) -> Point:
  delta = point.subtract_copy(origin)
  length = delta.length() - amt
  delta.normalize()
  delta.multiply(length)
  return origin.add_copy(delta)

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
  top = create_adjusted_point(pad_rect, top, params.top_range_x, params.top_range_y)
  left = create_adjusted_point(pad_rect, left, params.side_range_x, params.side_range_y)
  right = create_adjusted_point(pad_rect, right, params.side_range_x, params.side_range_y)

  # Recalc center
  cx = (top.x + left.x + right.x) / 3
  cy = (top.y + left.y + right.y) / 3
  center = Point(cx, cy)

  # Find length
  top_delta = top.subtract_copy(center)
  left_delta = left.subtract_copy(center)
  right_delta = right.subtract_copy(center)
  max_len = min(top_delta.length(), left_delta.length(), right_delta.length()) - params.shrink_amt

  i = 0
  while (True):
    points: List[Point] = []
    shrink = i * params.shrink_amt

    top_shrunk = shrink_vec(top, center, shrink)
    left_shrunk = shrink_vec(left, center, shrink)
    right_shrunk = shrink_vec(right, center, shrink)

    points.append(top_shrunk)
    points.append(left_shrunk)
    points.append(right_shrunk)
    points.append(top_shrunk)
    i = i + 1

    # draw_point_circles(points, group)
    if params.draw_triangles:
      draw_point_path(points, group)

    if shrink >= max_len:
      break

