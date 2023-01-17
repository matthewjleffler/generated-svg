from lib import *
from math import *


###
### Checkerboard Design
###

# TODO fill spaces

_deg_to_rad = pi / 180

class CheckerboardParams:
  def __init__(self) -> None:
    self.draw = True
    self.pad = 0
    self.size = RangeInt(10, 150)
    self.skew_vert_degs = RangeFloat(-45, 45)
    self.skew_horiz_degs = RangeFloat(-45, 45)

def line(p1:Point, p2:Point):
  A = (p1.y - p2.y)
  B = (p2.x - p1.x)
  C = (p1.x*p2.y - p2.x*p1.y)
  return A, B, -C

def intersection(L1, L2):
  D  = L1[0] * L2[1] - L1[1] * L2[0]
  Dx = L1[2] * L2[1] - L1[1] * L2[2]
  Dy = L1[0] * L2[2] - L1[2] * L2[0]
  if D != 0:
      x = Dx / D
      y = Dy / D
      return Point(x, y)
  else:
      return None

def _draw_line(start:Point, end:Point) -> str:
  return f"M{round(start.x, 2)} {round(start.y, 2)}L{round(end.x, 2)} {round(end.y, 2)}"

def _create_line_endpoints(
  origin_x:float,
  origin_y:float,
  vec:Point,
  pad_rect:Rect,
  l0, l1, l2, l3):

  origin_point = Point(origin_x, origin_y)
  vec = line(origin_point, origin_point.add_copy(vec))

  end_point = intersection(vec, l0)
  intersect_1 = intersection(vec, l1)
  if intersect_1 is not None:
    len_0 = end_point.subtract_copy(origin_point).length()
    len_1 = intersect_1.subtract_copy(origin_point).length()
    if len_1 < len_0:
      end_point = intersect_1

  # Cast backwards from end point to the top / left edge
  origin_point = intersection(vec, l2)
  intersect_3 = intersection(vec, l3)
  if intersect_3 is not None:
    len_2 = end_point.subtract_copy(origin_point).length()
    len_3 = end_point.subtract_copy(intersect_3).length()
    if len_3 < len_2:
      origin_point = intersect_3

  if not pad_rect.contains(origin_point.x, origin_point.y) and not pad_rect.contains(end_point.x, end_point.y):
    # Out of bounds
    return None

  return (origin_point, end_point)


def draw_checkerboard(params:CheckerboardParams, group:Group = None):
  # draw_border(group)

  # Pad safe space
  pad_rect = svg_safe().shrink_copy(params.pad)

  # Split the available space, pad excessively to ensure coverage
  # We throw away useless results
  size = params.size.rand()
  count_horiz = floor(svg_safe().w / size) * 2
  count_vert = floor(svg_safe().h / size) * 2
  count = max(count_horiz, count_vert)

  # Edge vectors
  edge_vec_horiz = Point(1, 0)
  edge_vec_vert = Point(0, 1)

  # Corner points
  corner_tl = Point(pad_rect.x, pad_rect.y)
  corner_bl = Point(pad_rect.x, pad_rect.bottom())
  corner_tr = Point(pad_rect.right(), pad_rect.y)

  # Edge lines
  line_bottom = line(corner_bl, corner_bl.add_copy(edge_vec_horiz))
  line_right = line(corner_tr, corner_tr.add_copy(edge_vec_vert))
  line_top = line(corner_tl, corner_tl.add_copy(edge_vec_horiz))
  line_left = line(corner_tl, corner_tl.add_copy(edge_vec_vert))

  # Skew Rads
  vert_degs = params.skew_vert_degs.rand()
  vert_rads = vert_degs * _deg_to_rad
  horiz_degs = params.skew_horiz_degs.rand()
  horiz_rads = horiz_degs * _deg_to_rad

  # Checkerboard vectors
  vert_vec = Point(0, 1)
  vert_vec = vert_vec.rotate_copy(vert_rads)

  horiz_vec = Point(1, 0)
  horiz_vec = horiz_vec.rotate_copy(horiz_rads)

  # Line points
  horiz: List[Point] = []
  vert: List[Point] = []

  # Create Lines
  for i in range(-count, count):
    # Cast from top edge
    origin_x = pad_rect.x + i * size
    origin_y = pad_rect.y

    mod = i % 2
    first = 0 + mod
    second = (1 + mod) % 2

    # Pick direction
    if vert_degs < 0:
      points = _create_line_endpoints(origin_x, origin_y, vert_vec, pad_rect,
                                      line_bottom, line_right, line_top, line_left)
      if points is not None:
        horiz.append(points[first])
        horiz.append(points[second])
    else:
      points = _create_line_endpoints(origin_x, origin_y, vert_vec, pad_rect,
                                      line_bottom, line_left, line_top, line_right)
      if points is not None:
        horiz.append(points[first])
        horiz.append(points[second])


    # Cast from left edge
    origin_x = pad_rect.x
    origin_y = pad_rect.y + i * size

    # Pick direction
    if horiz_degs < 0:
      points = _create_line_endpoints(origin_x, origin_y, horiz_vec, pad_rect,
                                      line_right, line_top, line_left, line_bottom)
      if points is not None:
        vert.append(points[first])
        vert.append(points[second])
    else:
      points = _create_line_endpoints(origin_x, origin_y, horiz_vec, pad_rect,
                                      line_right, line_bottom, line_left, line_top)
      if points is not None:
        vert.append(points[first])
        vert.append(points[second])

  # Draw horiz lines
  path = ""
  for i in range(0, len(horiz) - 1, 2):
    start = horiz[i]
    end = horiz[i + 1]
    path += _draw_line(start, end)

  # Draw vert lines
  for i in range(0, len(vert) - 1, 2):
    start = vert[i]
    end = vert[i + 1]
    path += _draw_line(start, end)

  if params.draw:
    draw_path(path, group)

