from lib import *
from lib_path import *
from lib_maze import *


###
### Triangle Design
###

class TriangleParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.debug_draw_boundary = True
    self.draw_triangles = True
    self.step_size = 5
    self.do_rotate = False
    self.rotate_range = RangeFloat(0, 180)
    self.do_shuffle = False
    self.shuffle_range = 100
    self.draw_background = True
    self.hatch_triangle = False
    self.hatch_background = False

    # Push params
    self.do_push: bool = True
    self.random_push: bool = False
    self.push_pad_range_max: float = .25
    self.push_pad_range_offset: float = 0
    self.push_num: RangeInt = RangeInt(800, 2000)
    self.push_range: RangeFloat = RangeFloat(400, 800)
    self.push_strength: RangeFloat = RangeFloat(0.5, 2.5) # TODOML scale?
    self.push_line_cell_size: RangeFloat = RangeFloat(100, 200)
    self.push_line_step_size = 10

    super().__init__(defaults)


def _create_adjusted_point(
  default:Point,
  params:TriangleParams
) -> Point:
  x_range = RangeInt(-params.shuffle_range, params.shuffle_range)
  y_range = RangeInt(-params.shuffle_range, params.shuffle_range)
  x_delta = x_range.rand()
  y_delta = y_range.rand()
  x = default.x + x_delta
  y = default.y + y_delta
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
    result += current
    next = scaled_corners[i + 1]

    current_line = Line(current[2], current[0])
    next_line = Line(next[0], next[1])
    intersection = line_intersection(current_line, next_line)
    if intersection is None:
      continue
    result.append(intersection)

  # Add the last ones in too
  result += scaled_corners[-1]

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
  pad_rect = svg_safe().copy()

  center = pad_rect.center()
  rot_rad = params.rotate_range.rand() * deg_to_rad

  side_len = pad_rect.h

  # Create base points
  top = Point(center.x, pad_rect.y)
  left = Point(0, 1).rotate(30 * deg_to_rad).multiply(side_len).add(top)
  right = Point(0, 1).rotate(-30 * deg_to_rad).multiply(side_len).add(top)

  # Rotate points
  if params.do_rotate:
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
  if params.do_shuffle:
    top = _create_adjusted_point(top, params)
    left = _create_adjusted_point(left, params)
    right = _create_adjusted_point(right, params)

  # Collect final corners, find center
  corners = [top, right, left]
  triangle_center = average_point(corners)

  # Find the shortest distance to center
  min_dist = maxsize
  for corner in corners:
    delta = triangle_center.subtract_copy(corner)
    dist = delta.length()
    min_dist = min(dist, min_dist)

  # Separate into steps
  count = floor(min_dist / params.step_size)
  dist_per = min_dist / count

  # Create point arrays
  triangle_points = _create_scaled_triangle_loop(triangle_center, corners, count, dist_per)
  # Separate edges into lines for later subdivision
  triangle_lines: List[List[Point]] = []
  for i in range(0, len(triangle_points) - 1):
    triangle_lines.append([triangle_points[i], triangle_points[i + 1]])

  # Find volume
  expand = ExpandingVolume(triangle_points)

  # Find how far to the left and right we need to draw
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad_rect)
  bg_width = (pad_rect.w / final_scale)

  # Draw background lines
  background_lines: List[List[Point]] = []
  bg_count = floor(bg_width / (params.step_size / 2))
  bg_sep = bg_width / bg_count
  line_left = Line(top, left)
  line_right = Line(top, right)
  for i in range(0, bg_count + 1):
    x = center.x - (bg_width / 2 ) + bg_sep * i
    line_current = Line(Point(x, top.y), Point(x, left.y))
    intersect_left = line_intersection(line_current, line_left)
    intersect_right = line_intersection(line_current, line_right)
    intersect_max = max(intersect_left.y, intersect_right.y)
    intersect_bottom = min(intersect_max - (params.step_size), left.y)
    if intersect_bottom < top.y:
      continue
    line_current.p1.y = intersect_bottom
    if i % 2 == 0:
      line_current.reverse()
    background_lines.append(line_current.points())

  # Subdivide all lines and collect them
  subdivision_range = RangeInt(100, 100)
  if params.do_push:
    for i in range(0, len(triangle_lines)):
      triangle_lines[i] = subdivide_point_path(triangle_lines[i], subdivision_range)
    for i in range(0, len(background_lines)):
      background_lines[i] = subdivide_point_path(background_lines[i], subdivision_range)
  push_rect = push_lines(triangle_lines + background_lines, pad_rect, params, group)

  # Re-encapsulate all the points and recaclulate scale
  expand.add_lists(triangle_lines)
  expand.add_lists(background_lines)
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad_rect)

  # Draw points
  if params.draw_triangles:
    parent = open_group(GroupSettings(), group)
    scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), parent)

    if params.debug_draw_boundary:
      draw_border(parent)
      draw_rect_rect(pad_rect, scaled)
      if params.do_push:
        draw_rect_rect(push_rect, scaled)
        draw_circ(push_rect.x, push_rect.y, 5, scaled)

    hatch_params = HatchParams(RangeInt(20, 50), RangeInt(3, 5))

    if params.hatch_triangle:
      # TODOML support for split versions?
      draw_point_path_hatched(triangle_points, hatch_params, scaled)
    else:
      for line in triangle_lines:
        centers = generate_centerpoints(line)
        draw_curved_path(line, centers, scaled)

    if params.draw_background:
      for line in background_lines:
        if params.hatch_background:
          draw_point_path_hatched(line, hatch_params, scaled)
        else:
          # draw_point_path(line, scaled)
          centers = generate_centerpoints(line)
          draw_curved_path(line, centers, scaled)

    close_group()
    close_group()

