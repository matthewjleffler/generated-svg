from lib import *


###
### Vertical Line Design
###


class VerticalLineParams(TypedDict):
  draw_highlights: bool
  draw_lines: bool
  mutate: bool
  draw_curves: bool # Curves or straight lines
  pad_x: float
  pad_y: float
  subdivide_range: RangeInt
  line_spacing: float
  rate_default: float
  shuffle_range_max_x: float
  shuffle_range_max_y: float
  strike_range: RangeInt
  circle_range: RangeInt
  mutate_range_x: float
  mutate_range_y: float
  mutate_max_range: float

  @classmethod
  def create(cls, defaults: Defaults) -> 'VerticalLineParams':
    result: VerticalLineParams = {
      'draw_highlights': True,
      'draw_lines': True,
      'mutate': False,
      'draw_curves': True,
      'pad_x': 100,
      'pad_y': 50,
      'subdivide_range': RangeInt(50, 70),
      'line_spacing': 5,
      'rate_default': 5,
      'shuffle_range_max_x': 40,
      'shuffle_range_max_y': 5,
      'strike_range': RangeInt(0, 10),
      'circle_range': RangeInt(0, 5),
      'mutate_range_x': 3,
      'mutate_range_y': 3,
      'mutate_max_range': 30,
    }
    return apply_defaults(result, defaults)


def _create_highlight(line:List[Point], left:float, final:float, params:VerticalLineParams, group:Group):
  available: List[int] = []
  claimed: List[int] = []

  group_blue = open_group(GroupSettings(stroke=GroupColor.blue), group)

  # Variables
  strike = params['strike_range'].rand()
  circles = params['circle_range'].rand()

  # Collect available indexes
  for i in range(1, len(line) - 1):
    available.append(i)

  # Create strikethroughs
  for _ in range(0, strike):
    i = rand_int(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if params['draw_highlights']:
      draw_path(f"M{svg_safe().x} {round(point.y, 2)}h{svg_safe().w}", group_blue)

  # Collect available indexes
  available = []
  origin = line[0]
  for i in range(1, len(line) - 1, 2):
    point = line[i]
    delta = point.x - origin.x
    if delta <= 10 or i in claimed:
      # Not available
      continue
    available.append(i)

  # Create circles
  for _ in range(0, circles):
    if len(available) < 1:
      break
    i = rand_int(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if params['draw_highlights']:
      draw_circ(left - 20, point.y, 10, group_blue)

  # Create starbursts
  available = []
  for i in range(1, len(line) - 1, 2):
    point = line[i]
    delta = point.x - origin.x
    if delta >= -10 or i in claimed:
      # Not available
      continue
    available.append(i)

  # Create sunbursts
  for _ in range(0, circles):
    if len(available) < 1:
      break
    i = rand_int(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if params['draw_highlights']:
      draw_sunburst(10, final + 20, point.y, 10, 5, group)

def _create_lines(params:VerticalLineParams, group:Group):
  pad_rect = svg_safe().shrink_xy_copy(params['pad_x'], params['pad_y'])

  # Pick subdivisions, make sure it's an even number
  subdivide = params['subdivide_range'].rand()
  if subdivide % 2 == 1:
    subdivide += 1

  space = params['line_spacing']
  rate = space / params['rate_default']
  line_count = floor(pad_rect.w / space)

  # Create first line
  rough: List[Point] = []
  rough.append(Point(0, pad_rect.y))
  rough.append(Point(0, pad_rect.bottom()))

  # Subdivide
  fine = subdivide_point_path(rough, RangeInt(subdivide, subdivide))

  # Shuffle odd points
  for i in range(1, len(fine), 2):
    fine_point = fine[i]
    fine_point.x += rand_float(-params['shuffle_range_max_x'], params['shuffle_range_max_x'])
    fine_point.y += rand_float(-params['shuffle_range_max_y'], params['shuffle_range_max_y'])

  # Duplicate line
  mutate_range_x = params['mutate_range_x'] * rate
  mutate_range_y = params['mutate_range_y'] * rate
  max_range = params['mutate_max_range']

  space = pad_rect.w / line_count
  lines: List[List[Point]] = []
  for i in range(0, line_count):
    line: List[Point] = []
    lines.append(line)
    for j in range(0, len(fine)):
      fine_point = fine[j]
      point = Point(round(pad_rect.x + fine_point.x + space * i, 2), round(fine_point.y, 2))
      line.append(point)

      if params['mutate']:
        if j % 2 == 1:
          mutate_amt_x = rand_float(-mutate_range_x, mutate_range_x)
          fine_point.x = clamp(fine_point.x + mutate_amt_x, -max_range, max_range)

        mutate_amt_y = rand_float(-mutate_range_y, mutate_range_y)
        fine_point.y = clamp(fine_point.y + mutate_amt_y, pad_rect.y, pad_rect.bottom())

  # Draw curves
  for j in range(0, len(lines)):
    line = lines[j]

    if j % 2 == 0:
      point = line[0]
      path_val = f"M{point.x} {point.y}"

      if params['draw_curves']:
        for i in range(1, len(line) - 1, 2):
          control = line[i]
          point = line[i + 1]
          path_val += f"Q{control.x} {control.y} {point.x} {point.y}"
      else:
        for i in range(1, len(line)):
          point = line[i]
          path_val += f"L{point.x} {point.y}"

    else:
      point = line[-1]
      path_val = f"M{point.x} {point.y}"

      if params['draw_curves']:
        for i in range(len(line) - 2, 0, -2):
          control = line[i]
          point = line[i - 1]
          path_val += f"Q{control.x} {control.y} {point.x} {point.y}"
      else:
        for i in range(len(line) - 1, 0):
          point = line[i]
          path_val += f"L{point.x} {point.y}"

    if params['draw_lines']:
      draw_path(path_val, group)

  return (fine, lines[0][0].x, lines[-1][0].x)


def draw_lines(params:VerticalLineParams, group:Group):
  reload_libs(globals())

  # draw_border(group)

  result = _create_lines(params, group)
  _create_highlight(result[0], result[1], result[2], params, group)
