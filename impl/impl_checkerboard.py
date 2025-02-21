from lib import *


###
### Checkerboard Design
###

class CheckerboardParams(TypedDict):
  draw_lines: bool
  draw_aligned_vertical: bool
  draw_aligned_horizontal: bool
  draw_filled_checkers: bool
  pad: int
  size: RangeInt
  skew_vert_degs: RangeFloat
  skew_horiz_degs: RangeFloat
  interior_space_aligned: float
  interior_space_filled: float
  mutate_checkers: bool

  @classmethod
  def create(cls, defaults: Defaults) -> 'CheckerboardParams':
    result: CheckerboardParams = {
      'draw_lines': True,
      'draw_aligned_vertical': True,
      'draw_aligned_horizontal': True,
      'draw_filled_checkers': True,
      'pad': 0,
      'size': RangeInt(10, 150),
      'skew_vert_degs': RangeFloat(0, 45),
      'skew_horiz_degs': RangeFloat(0, 45),
      'interior_space_aligned': 5,
      'interior_space_filled': 5,
      'mutate_checkers': True,
    }
    return apply_defaults(result, defaults)


class Checker:
  def __init__(self, left:Line, right:Line, top:Line, bottom:Line) -> None:
    self.top = top
    self.bottom = bottom
    self.left = left
    self.right = right
    self.tl = line_intersection(top, left)
    self.br = line_intersection(bottom, right)
    self.tr = line_intersection(top, right)
    self.bl = line_intersection(bottom, left)
    self.center = self.br.subtract_copy(self.tl)
    centerlen = self.center.length() * .5
    self.center.normalize()
    self.center.multiply(centerlen)
    self.center = self.tl.add_copy(self.center)

  def __lt__(self, other):
    return self.center.__lt__(other.center)

  def visible(self, rect:Rect) -> bool:
    if rect.contains_point(self.tl):
      return True
    if rect.contains_point(self.tr):
      return True
    if rect.contains_point(self.br):
      return True
    if rect.contains_point(self.bl):
      return True
    return False

def _draw_line(start:Point, end:Point) -> str:
  return f"M{round(start.x, 2)} {round(start.y, 2)}L{round(end.x, 2)} {round(end.y, 2)}"

def _create_point_path_alternating(list:List[Point]) -> str:
  path = ""
  for i in range(0, len(list) - 1, 2):
    mod = floor(i / 2) % 2
    first = mod
    second = (mod + 1) % 2
    start = list[i + first]
    end = list[i + second]
    path += _draw_line(start, end)
  return path

def _create_line_endpoints(
  origin_x:float,
  origin_y:float,
  vec:Point,
  pad_rect:Rect,
  lines:List):

  origin_point = Point(origin_x, origin_y)
  vec_line = Line(origin_point, origin_point.add_copy(vec))

  end_point = _pick_closest_intersection(origin_point, vec_line, [lines[0], lines[1]])
  origin_point = _pick_closest_intersection(end_point, vec_line, [lines[2], lines[3]])

  if not pad_rect.contains(origin_point.x, origin_point.y) and not pad_rect.contains(end_point.x, end_point.y):
    # Out of bounds
    return None

  return (origin_point, end_point)

def _pick_bottom_intersection(checker_bounds:Rect, intersections:List[Point]) -> Point:
  max = -maxsize
  result = None
  for i in intersections:
    if i is None:
      continue
    if not checker_bounds.contains(i.x, i.y):
      # Not a valid result
      continue
    if i.y > max:
      max = i.y
      result = i
  return result

def _pick_top_intersection(checker_bounds:Rect, intersections:List[Point]) -> Point:
  min = maxsize
  result = None
  for i in intersections:
    if i is None:
      continue
    if not checker_bounds.contains(i.x, i.y):
      # Not a valid result
      continue
    if i.y < min:
      min = i.y
      result = i
  return result

def _pick_closest_intersection(origin:Point, line, others) -> Point:
  result = None
  min = maxsize
  for other in others:
    point = line_intersection(line, other)
    if point is None:
      continue
    dist = point.subtract_copy(origin)
    length = dist.length()
    if length < min:
      min = length
      result = point
  return result

def _create_fill(
  vec:Point,
  pad_rect:Rect,
  checker:Checker, bounds, checker_fill:List[Point],
  params:CheckerboardParams) -> List[Point]:

  left = checker.left
  right = checker.right
  top = checker.top
  bottom = checker.bottom
  bounds_top = bounds[0]
  bounds_bottom = bounds[1]

  top_left = line_intersection(left, top)
  top_right = line_intersection(right, top)
  bottom_left = line_intersection(left, bottom)
  bottom_right = line_intersection(right, bottom)

  min_x = min(top_left.x, top_right.x, bottom_left.x, bottom_right.x)
  max_x = max(top_left.x, top_right.x, bottom_left.x, bottom_right.x)
  min_y = min(top_left.y, top_right.y, bottom_left.y, bottom_right.y)
  max_y = max(top_left.y, top_right.y, bottom_left.y, bottom_right.y)

  space_x = max_x - min_x
  space_y = max_y - min_y
  count = floor(space_x / params['interior_space_filled'])
  real_dist = space_x / count
  valid_rect = Rect(min_x, min_y, space_x, space_y)

  for i in range(1, count):
    origin_x = min_x + real_dist * i
    origin_y = min_y - 10

    origin = Point(origin_x, origin_y)
    stroke_line = Line(origin, origin.add_copy(vec))

    l_intersect = line_intersection(stroke_line, left)
    r_intersect = line_intersection(stroke_line, right)
    t_intersect = line_intersection(stroke_line, top)
    b_intersect = line_intersection(stroke_line, bottom)
    intersections = [l_intersect, r_intersect, t_intersect, b_intersect]

    # Check validity as we go
    start = _pick_top_intersection(valid_rect, intersections)
    if start is None:
      continue
    end = _pick_bottom_intersection(valid_rect, intersections)
    if end is None:
      continue

    # Out of bounds
    if start.x < pad_rect.x or start.x > pad_rect.right() or end.y < pad_rect.y or start.y > pad_rect.bottom():
      continue

    # Test top and bottom intersections
    top_intersection = line_intersection(stroke_line, bounds_top)
    if top_intersection.y > start.y:
      start = top_intersection

    bottom_insection = line_intersection(stroke_line, bounds_bottom)
    if bottom_insection.y < end.y:
      end = bottom_insection

    checker_fill.append(start)
    checker_fill.append(end)

    # draw_path(f"M{start.x} {start.y}L{end.x} {end.y}")



def draw_checkerboard(params:CheckerboardParams, group:Group):
  reload_libs(globals())

  # draw_border(group)

  # Pad safe space
  pad_rect = svg_safe().shrink_copy(params['pad'])

  # Split the available space, pad excessively to ensure coverage
  # We throw away useless results
  size = params['size'].rand()
  count_horiz = floor(svg_safe().w / size) * 2
  count_vert = floor(svg_safe().h / size) * 2
  count = max(count_horiz, count_vert)

  shift_x_range = RangeFloat(-30, 30) # TODO move to params
  shift_x = shift_x_range.rand()

  shift_y_range = RangeFloat(-30, 30) # TODO params
  shift_y = shift_y_range.rand()

  # print(shift_x, shift_y)

  corners: List[Point] = []
  for y in range(-count_vert, count_vert * 2):
    for x in range(-count_horiz, count_horiz * 2):
      point = Point(x * size + shift_x * x, y * size + shift_y)
      corners.append(point)

  # print(len(corners))

  for i in range(0, len(corners)):
    point = corners[i]
    draw_circ(point.x, point.y, 5, group)
    # open_group(GroupSettings(translatePoint=point, scale=0.5))
    # draw_text(0, 0, 5, str(i))
    # close_group()

  return

  # Edge vectors
  edge_vec_horiz = Point(1, 0)
  edge_vec_vert = Point(0, 1)

  # Corner points
  corner_tl = Point(pad_rect.x, pad_rect.y)
  corner_bl = Point(pad_rect.x, pad_rect.bottom())
  corner_tr = Point(pad_rect.right(), pad_rect.y)

  # Edge lines
  line_bottom = Line(corner_bl, corner_bl.add_copy(edge_vec_horiz))
  line_right = Line(corner_tr, corner_tr.add_copy(edge_vec_vert))
  line_top = Line(corner_tl, corner_tl.add_copy(edge_vec_horiz))
  line_left = Line(corner_tl, corner_tl.add_copy(edge_vec_vert))

  # Skew Rads
  vert_degs = params['skew_vert_degs'].rand()
  vert_rads = vert_degs * deg_to_rad
  horiz_degs = params['skew_horiz_degs'].rand()
  horiz_rads = horiz_degs * deg_to_rad

  # Checkerboard vectors
  vert_vec = Point(0, 1)
  vert_vec = vert_vec.rotate_copy(vert_rads)

  horiz_vec = Point(1, 0)
  horiz_vec = horiz_vec.rotate_copy(horiz_rads)

  fill_vec = Point(0, 1)

  # Line points
  vert: List[Point] = []
  vert_lines = []
  horiz: List[Point] = []
  horiz_lines = []

  lines_vert = [line_bottom, line_right, line_top, line_left]
  if vert_degs > 0:
    lines_vert = [line_bottom, line_left, line_top, line_right]
  lines_horiz = [line_right, line_top, line_left, line_bottom]
  if horiz_degs > 0:
    lines_horiz = [line_right, line_bottom, line_left, line_top]

  # Create Lines
  for i in range(-count, count):
    # Cast from top edge
    origin_x = pad_rect.x + i * size
    origin_y = pad_rect.y

    # Store line for later
    vert_line = Line(Point(origin_x, origin_y), Point(origin_x + vert_vec.x, origin_y + vert_vec.y))
    vert_lines.append(vert_line)

    # Create rendering points
    points = _create_line_endpoints(origin_x, origin_y, vert_vec, pad_rect, lines_vert)
    if points is not None:
      vert.append(points[0])
      vert.append(points[1])

    # Cast from left edge
    origin_x = pad_rect.x
    origin_y = pad_rect.y + i * size

    # Store line for later
    horiz_line = Line(Point(origin_x, origin_y), Point(origin_x + horiz_vec.x, origin_y + horiz_vec.y))
    horiz_lines.append(horiz_line)

    # Create rendering points
    points = _create_line_endpoints(origin_x, origin_y, horiz_vec, pad_rect, lines_horiz)
    if points is not None:
      horiz.append(points[0])
      horiz.append(points[1])

  # Draw primary lines
  if params['draw_lines']:
    path = _create_point_path_alternating(vert)
    path += _create_point_path_alternating(horiz)
    draw_path(path, group)

  # Interior fill
  fill_count_per = floor(size / params['interior_space_aligned'])
  offset_space = size / fill_count_per
  fill_vert: List[Point] = []
  fill_horiz: List[Point] = []

  # Step through and create aligned fill
  for i in range(0, len(vert), 4):
    start = vert[i]
    # Create interior aligned fill
    for j in range(1, fill_count_per):
      offset = j * offset_space
      points = _create_line_endpoints(start.x + offset, start.y, vert_vec, pad_rect, lines_vert)
      if points is not None:
        fill_vert.append(points[0])
        fill_vert.append(points[1])

  for i in range(0, len(horiz), 4):
    start = horiz[i]
    # Create interior aligned fill
    for j in range(1, fill_count_per):
      offset = j * offset_space
      points = _create_line_endpoints(start.x, start.y + offset, horiz_vec, pad_rect, lines_horiz)
      if points is not None:
        fill_horiz.append(points[0])
        fill_horiz.append(points[1])

  # Draw interior aligned lines
  if params['draw_aligned_vertical']:
    group_red = open_group(GroupSettings(stroke=GroupColor.red), group)
    path = _create_point_path_alternating(fill_vert)
    draw_path(path, group_red)

  if params['draw_aligned_horizontal']:
    group_blue = open_group(GroupSettings(stroke=GroupColor.blue), group)
    path = _create_point_path_alternating(fill_horiz)
    draw_path(path, group_blue)


  # Step through and create checkerboard sets
  checkers: List[Checker] = []
  checker_fill: List[Point] = []

  # Add vertical checkers
  for i in range(0, len(vert_lines) - 1, 2):
    checker_left = vert_lines[i]
    checker_right = vert_lines[i + 1]
    for j in range(0, len(horiz_lines) - 1, 2):
      checker_top = horiz_lines[j]
      checker_bottom = horiz_lines[j + 1]
      checkers.append(Checker(checker_left, checker_right, checker_top, checker_bottom))

  # Add horizontal checkers
  for i in range(1, len(horiz_lines) - 1, 2):
    checker_top = horiz_lines[i]
    checker_bottom = horiz_lines[i + 1]
    for j in range(1, len(vert_lines) - 1, 2):
      checker_left = vert_lines[j]
      checker_right = vert_lines[j + 1]
      checkers.append(Checker(checker_left, checker_right, checker_top, checker_bottom))

  # Cull and sort checkers
  i = len(checkers)
  while i > 0:
    i = i - 1
    checker = checkers[i]
    if not checker.visible(pad_rect):
      checkers.pop(i)
  checkers.sort()

  # Debug draw checker centers
  # for i in range(0, len(checkers)):
  #   checker = checkers[i]
  #   center = checker.center
  #   draw_circ(center.x, center.y, 5, group)
  #   scale = 0.3
  #   text_group = open_group(GroupSettings(translatePoint=center, scale=scale))
  #   draw_text(0, 0, 5, str(i), text_group)

  # Create checker fill points
  top_bottom = [line_top, line_bottom]
  for i in range(0, len(checkers)):
    checker = checkers[i]
    _create_fill(fill_vec, pad_rect, checker, top_bottom, checker_fill, params)

  if params['draw_filled_checkers']:
    group_green = open_group(GroupSettings(stroke=GroupColor.green), group)
    path = _create_point_path_alternating(checker_fill)
    draw_path(path, group_green)

  # Collect checker corner points
  corners: List[Point] = []
  for checker in checkers:
    add_nondup_point(checker.tl, corners)
    add_nondup_point(checker.tr, corners)
    add_nondup_point(checker.br, corners)
    add_nondup_point(checker.bl, corners)

  corners.sort()

  # Debug draw corners
  for i in range(0, len(corners)):
    corner = corners[i]
    draw_circ(corner.x, corner.y, 5, group)
    scale = 0.3
    open_group(GroupSettings(translate=(corner.x, corner.y), scale=scale), group)
    draw_text(0, 0, 5, str(i), group)
