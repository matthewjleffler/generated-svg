from lib import *


###
### Worm Drawing
###


# Small Repeated Worm Pattern

class WormParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw_worm = True
    self.draw_innards = True
    self.padding = 50
    self.stack_count = 50
    self.size_range = RangeInt(5, 100)
    self.stack_spread = 3
    self.fixed_size = 5

    super().__init__(defaults)


def _draw_worm_set(
  max_row:int,
  max_col:int,
  worm_size:int,
  fixed_size:float,
  params:WormParams,
  group:Group
):

  for row in range(0, max_row):
    origin_y = worm_size * row * 1.5

    for col in range(0, max_col):
      max_size = params.size_range.rand()
      origin_x = worm_size * col

      # Debug bounds
      # draw_rect(svg_safe().x + origin_x, svg_safe().y + origin_y, params.worm_size, params.worm_size, group)

      for i in range(0, params.stack_count + 1):
        percent = i / params.stack_count
        pi_percent = percent * pi
        pi_half_percent = percent * pi * .25

        size = sin(pi_percent) * max_size
        if fixed_size != 0:
          size = min(fixed_size, size)

        half = size / 2

        x = svg_safe().x + origin_x + sin(pi_half_percent) * params.stack_spread * i
        y = svg_safe().y + origin_y + cos(pi_half_percent) * params.stack_spread * i

        draw_circ(x, y, half, group)

def _draw_worm_layer(params:WormParams, fixed_size:float, group:Group):
  worm_size = params.stack_count * params.stack_spread * .75
  worm_row_size = worm_size * 1.55

  pad_x = svg_safe().w - params.padding
  pad_y = svg_safe().h - params.padding

  max_col = floor(pad_x / worm_size)
  max_row = floor(pad_y / worm_row_size)

  offset_x = round((svg_safe().w - (max_col * worm_size)) / 2, 2)
  offset_y = round((svg_safe().h - (max_row * worm_row_size)) / 2, 2)

  group_offset = open_group(GroupSettings(translate=(offset_x, offset_y)), group)
  _draw_worm_set(max_row, max_col, worm_size, fixed_size, params, group_offset)
  translate_x = svg_full().w - offset_x + worm_size * .1
  translate_y = offset_y + worm_size * .75
  group_flipped = open_group(GroupSettings(translate=(translate_x, translate_y), scaleXY=(-1, 1)), group)
  _draw_worm_set(max_row, max_col, worm_size, fixed_size, params, group_flipped)

def draw_worm(params:WormParams, group:Group):
  reload_libs(globals())

  # draw_border(group)

  if params.draw_worm:
    _draw_worm_layer(params, 0, group)

  if params.draw_innards:
    group_blue = open_group(GroupSettings(stroke=GroupColor.blue), group)
    _draw_worm_layer(params, params.fixed_size, group_blue)


# Long Worm Random Winding

class LongWormParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    # Draw
    self.draw_worm = True
    self.draw_highlight = True

    # Setup variables
    self.step_dist = 5 # How far (roughly) between steps
    self.circle = True # Render circles or squares

    # Layout generation
    self.peaks = RangeInt(3, 7)
    self.shuffle_large_max_x = 80
    self.shuffle_large_max_y = 100
    self.shuffle_small_max_x = 30
    self.shuffle_small_max_y = 30
    self.rough_subdivisions = RangeInt(1, 10)
    self.padding = 100

    # Worm circle sizes
    self.size_end = 1
    self.size_range = RangeInt(5, 60)

    # Highlights
    self.highlight_end_circle_radius = 30
    self.highlight_end_points = 10
    self.highlight_end_point_radius = 5
    self.highlight_sunburst_ray_len = 10

    self.highlights = RangeInt(3, 5)

    self.highlight_padding = 20
    self.consumed_check_radius = 50
    self.highlight_spacing = 10

    self.highlight_text_weight = [
      (0, 1), (1, 3),
    ]
    self.highlight_text_num_range = RangeInt(200, 50000)
    self.connect_highlight_weight = [
      (0, 1), (1, 3),
    ]

    self._apply_params(defaults)

class HighlightType(IntEnum):
  Circle = 0
  DoubleRing = 1,
  SunRing = 2,

  End = 3,

def _check_point_consumed(position:Position, consumed_highlights:List[Position], params:LongWormParams) -> bool:
  point = position.point()
  for consumed in consumed_highlights:
    vec = consumed.point()
    vec = vec.subtract_copy(point)

    len = vec.length()
    size = position.size + consumed.size + params.consumed_check_radius + params.highlight_padding * 2
    if len < size:
      return True
  return False

def _pick_valid_highlight(available_highlights:List[int], consumed_highlights:List[Position], positions:List[Position], params:LongWormParams):
  while True:
    index = rand_int(0, len(available_highlights) - 1)
    index = available_highlights.pop(index)
    position = positions[index]

    consumed = _check_point_consumed(position, consumed_highlights, params)
    if not consumed:
      # We're good, consume the point
      consumed_highlights.append(position)
      return position

    # Are we out of points?
    if len(available_highlights) < 1:
      return None

def _draw_worm_highlights(positions:List[Position], params:LongWormParams, group:Group):
  group_blue = open_group(GroupSettings(stroke=GroupColor.blue), group)

  start = positions[0]
  end = positions[-1]

  # Draw rings
  if params.draw_highlight:
    draw_ring_of_circles(params.highlight_end_points, start.x, start.y, params.highlight_end_circle_radius, params.highlight_end_point_radius, group_blue)
    draw_sunburst(params.highlight_end_points, end.x, end.y, params.highlight_end_circle_radius, params.highlight_sunburst_ray_len, group_blue)
    # draw_ring_of_circles(params.highlight_end_points, end.x, end.y, params.highlight_end_circle_radius, params.highlight_end_point_radius, group_blue)

  consumed_highlights = []
  consumed_highlights.append(Position(start.x, start.y, params.highlight_end_circle_radius))
  consumed_highlights.append(Position(end.x, end.y, params.highlight_end_circle_radius))

  available_highlights = []
  for i in range(0, len(positions)):
    available_highlights.append(i)

  # highlight_size = size_max + 10
  highlight_count = params.highlights.rand()

  connect_next = False
  last = Point(0,0)

  while highlight_count > 0:
    # Pick valid highlight
    point = _pick_valid_highlight(available_highlights, consumed_highlights, positions, params)
    if point is None:
      return # Ran out of points

    num = 0
    # Decide whether to render a number
    if rand_weight(params.highlight_text_weight) == 0:
      # Pick number to render
      num = params.highlight_text_num_range.rand()

    # Pick random highlight type
    highlight_index = rand_int(0, int(HighlightType.End - 1))
    highlight_type = HighlightType(highlight_index)

    highlight_count -= 1
    highlight_size = point.size + params.highlight_padding

    if params.draw_highlight:
      if connect_next:
        draw_path(f"M {last.x} {last.y}L{point.x} {point.y}", group_blue)

      if highlight_type == HighlightType.Circle:
        draw_circ(point.x, point.y, highlight_size, group_blue)
      elif highlight_type == HighlightType.DoubleRing:
        draw_circ(point.x, point.y, highlight_size, group_blue)
        draw_circ(point.x, point.y, highlight_size + params.highlight_spacing, group_blue)
      elif highlight_type == HighlightType.SunRing:
        draw_circ(point.x, point.y, highlight_size, group_blue)
        draw_sunburst(20, point.x, point.y, highlight_size + params.highlight_spacing, params.highlight_spacing, group_blue)

      if num > 0:
        group_text = open_group(GroupSettings(translate=(point.x + highlight_size * 1.5, point.y), scale=0.5), group_blue)
        draw_text(0, 0, 10, str(num), group_text)

    last = point
    # Decide whether to connect the next line
    connect_next = rand_weight(params.connect_highlight_weight) == 0

def draw_long_worm(params:LongWormParams, group:Group):
  reload_libs(globals())

  # draw_border(group)

  # Variables
  peaks = params.peaks.rand()
  top_first = rand_bool()

  # Build outline
  pad_rect = svg_safe().shrink_copy(params.padding)

  # Subdivide space
  space = pad_rect.w / (peaks + 1)

  # Pick direction of motion
  if top_first:
    first = pad_rect.y
    second = pad_rect.bottom()
  else:
    first = pad_rect.bottom()
    second = pad_rect.y

  # Pick rough points
  rough_points: List[Point] = []
  rough_points.append(Point(pad_rect.x, pad_rect.center_y()))
  for i in range(0, peaks):
    rough_points.append(Point(pad_rect.x + space * (i + 1), first))
    rough_points.append(Point(pad_rect.x + space * (i + 1), second))
  rough_points.append(Point(pad_rect.right(), pad_rect.center_y()))

  # Shuffle rough points
  shuffle_points(params.shuffle_large_max_x, params.shuffle_large_max_y, rough_points)

  # Draw rough points
  # draw_point_path(rough_points, group)

  # Subdivide rough path
  points = subdivide_point_path(rough_points, params.rough_subdivisions, [1, len(rough_points) - 1])

  # Shuffle subdivided path
  shuffle_points(params.shuffle_small_max_x, params.shuffle_small_max_y, points)

  # Draw subdivided points
  # draw_point_path(points, group)

  centers = generate_centerpoints(points)
  # draw_curved_path(points, centers)
  positions = generate_final_positions(points, centers, params.size_end, params.size_range, params.step_dist)

  # Draw actual items created in last loop
  if params.draw_worm:
    for pos in positions:
      if params.circle:
        draw_circ(pos.x, pos.y, pos.size, group)
      else:
        draw_rect(pos.x - pos.size, pos.y - pos.size, pos.size * 2, pos.size * 2, group)

  _draw_worm_highlights(positions, params, group)


# Spiral Worm Drawing

class SpiralWormBorderType(Enum):
  Empty = 0
  Sunburst = 1
  Circles = 2


class SprialWormParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw_worm = True
    self.draw_highlight = True
    self.draw_highlight2 = True
    self.ring_distance = 10
    self.weight_rings = [
      (0, 1), (1, 1), (2, 0.5), (3, 0.1), (4, 0.05)
    ]
    self.weight_border = [
      (SpiralWormBorderType.Empty, 1), (SpiralWormBorderType.Sunburst, 0.5), (SpiralWormBorderType.Circles, 0.5)
    ]
    self.h2_size = RangeInt(25, 100)
    self.padding = 100
    self.spiral_rows = 4
    self.points_per_ring = 10
    self.rough_shuffle_range = 20
    self.fine_shuffle_range = 30
    self.rough_clamp_distance = 30
    self.subdivision_range = RangeInt(3, 7)
    self.position_range = RangeInt(1, 50)
    self.position_steps = 5
    self.ring_range = RangeInt(1, 4)

    self._apply_params(defaults)


def _spiral_worm_highlight(
  height:float,
  x:float,
  y:float,
  params:SprialWormParams,
  group:Group
):

  rings = rand_weight(params.weight_rings)
  half_height = height / 2
  if params.draw_highlight:
    for i in range(0, rings):
      draw_circ(x, y, half_height + params.ring_distance * i, group)

  max_ring = half_height + params.ring_distance * rings
  border = rand_weight(params.weight_border)
  if params.draw_highlight:
    if border == SpiralWormBorderType.Empty:
      pass
    elif border == SpiralWormBorderType.Circles:
      draw_ring_of_circles(100, x, y, max_ring, 5, group)
    elif border == SpiralWormBorderType.Sunburst:
      draw_sunburst(100, x, y, max_ring, 15, group)


def _highlight_2(
  width:float,
  height:float,
  x:float,
  y:float,
  positions:List[Position],
  params:SprialWormParams,
  group:Group
):
  center = (width - height)

  size = params.h2_size.rand()
  left_rings = params.ring_range.rand()
  left_circ_x = x - center

  size = params.h2_size.rand()
  right_rings = params.ring_range.rand()
  right_circ_x = x + center

  pos_index = rand_int(0, len(positions) - 1)
  pos = positions[pos_index]
  path = "M{} {}L{} {}L{} {}".format(left_circ_x, y, pos.x, pos.y, right_circ_x, y)

  if params.draw_highlight2:
    for i in range(0, left_rings):
      draw_circ(left_circ_x, y, size + 10 * i, group)
    for i in range(0, right_rings):
      draw_circ(right_circ_x, y, size + 10 * i, group)
    draw_path(path, group)
    draw_circ(pos.x, pos.y, pos.size + 10, group)


def draw_spiral_worm(params:SprialWormParams, group:Group):
  reload_libs(globals())

  # draw_border()

  # Build outline
  pad_rect = svg_safe().shrink_copy(params.padding)

  # Spiral settings
  spacing = pad_rect.h / (params.spiral_rows * 4)
  total_points = params.points_per_ring * params.spiral_rows
  rand_offset = rand() * pi * 2

  # Generate rough points
  rough_points: List[Point] = []
  for i in range(0, total_points):
    spiral = floor(i / params.points_per_ring) / params.spiral_rows
    in_row = (i % params.points_per_ring) / params.points_per_ring

    dist = spiral * params.points_per_ring * spacing + in_row * spacing * 2

    rads = in_row * pi * 2
    x = pad_rect.center_x() + cos(rads + rand_offset) * dist
    y = pad_rect.center_y() + sin(rads + rand_offset) * dist
    rough_points.append(Point(x, y))

  # Shuffle rough points
  shuffle_points(params.rough_shuffle_range, params.rough_shuffle_range, rough_points)

  # Draw rough points
  # draw_point_circles(rough_points, group)
  # draw_point_path(rough_points, group)

  # Subdivide path into final points
  points = subdivide_point_path(rough_points, params.subdivision_range, [1, len(rough_points) - 1])

  # Cull close points
  clamp_point_list(params.rough_clamp_distance, points)
  clean_duplicates(points)

  # Shuffle fine points
  shuffle_points(params.fine_shuffle_range, params.fine_shuffle_range, points)

  clamp_point_list(1, points)
  clean_duplicates(points)

  # Draw fine points
  # draw_point_circles(points, group)
  # draw_point_path(points, group)

  # Generate curve
  centers = generate_centerpoints(points)

  # Draw curve
  # draw_curved_path(points, centers, group)

  # Generate positions
  positions = generate_final_positions(points, centers, 1, params.position_range, params.position_steps)

  if params.draw_worm:
    for pos in positions:
      draw_circ(pos.x, pos.y, pos.size, group)

  group_blue = open_group(GroupSettings(stroke=GroupColor.blue), group)
  _spiral_worm_highlight(pad_rect.h, pad_rect.center_x(), pad_rect.center_y(), params, group_blue)

  group_red = open_group(GroupSettings(stroke=GroupColor.red), group)
  _highlight_2(pad_rect.w, pad_rect.h, pad_rect.center_x(), pad_rect.center_y(), positions, params, group_red)

