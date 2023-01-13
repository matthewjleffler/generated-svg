from lib import *
from path import *
from text import *
from enum import IntEnum


class WormParams:
  def __init__(self) -> None:
    self.padding = 50
    self.stack_count = 50
    self.size_range = RangeInt(5, 100)
    self.stack_spread = 3
    self.fixed_size = 0
    self.max_row = self.max_col = self.worm_size = 0

def _draw_worm_set(params:WormParams):
  for row in range(0, params.max_row):
    origin_y = params.worm_size * row * 1.5

    for col in range(0, params.max_col):
      max_size = params.size_range.rand()
      origin_x = params.worm_size * col

      # Debug bounds
      # draw_rect(svg_safe().x + origin_x, svg_safe().y + origin_y, params.worm_size, params.worm_size)

      for i in range(0, params.stack_count + 1):
        percent = i / params.stack_count
        pi_percent = percent * pi
        pi_half_percent = percent * pi * .25

        size = sin(pi_percent) * max_size
        if params.fixed_size != 0:
          size = min(params.fixed_size, size)

        half = size / 2

        x = svg_safe().x + origin_x + sin(pi_half_percent) * params.stack_spread * i
        y = svg_safe().y + origin_y + cos(pi_half_percent) * params.stack_spread * i

        draw_circ(x, y, half)

def draw_worm(params:WormParams):
  params.worm_size = params.stack_count * params.stack_spread * .75
  worm_row_size = params.worm_size * 1.55

  pad_x = svg_safe().w - params.padding
  pad_y = svg_safe().h - params.padding

  params.max_col = floor(pad_x / params.worm_size)
  params.max_row = floor(pad_y / worm_row_size)

  offset_x = (svg_safe().w - (params.max_col * params.worm_size)) / 2
  offset_y = (svg_safe().h - (params.max_row * worm_row_size)) / 2

  open_group("transform=\"translate({},{})\"".format(offset_x, offset_y))
  _draw_worm_set(params)
  close_group()
  open_group("transform=\"translate({},{}) scale(-1,1)\""
    .format(svg_full().w - offset_x + params.worm_size * .1, offset_y + params.worm_size * .75))
  _draw_worm_set(params)
  close_group()


class LongWormParams:
  def __init__(self) -> None:
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

    # Worm circle sizes
    self.size_end = 1
    self.size_min = 5
    self.size_max = 60

    # Highlights
    self.highlight_end_circle_radius = 30
    self.highlight_end_points = 10
    self.highlight_end_point_radius = 5

    self.highlights = RangeInt(3, 5)

    self.highlight_padding = 20
    self.consumed_check_radius = 50

    # Draw
    self.draw_worm = True
    self.draw_highlight = True

class HighlightType(IntEnum):
  Circle = 0
  DoubleRing = 1,
  SunRing = 2,

  End = 3,

def check_point_consumed(position:Position, consumed_highlights:List[Position], params:LongWormParams) -> bool:
  point = position.point()
  for consumed in consumed_highlights:
    vec = consumed.point()
    vec = vec.subtract_copy(point)

    len = vec.length()
    size = position.size + consumed.size + params.consumed_check_radius + params.highlight_padding * 2
    if len < size:
      return True
  return False

def pick_valid_highlight(available_highlights:List[int], consumed_highlights:List[Position], positions:List[Position], params:LongWormParams):
  while True:
    index = rand_int(0, len(available_highlights) - 1)
    index = available_highlights.pop(index)
    position = positions[index]

    consumed = check_point_consumed(position, consumed_highlights, params)
    if not consumed:
      # We're good, consume the point
      consumed_highlights.append(position)
      return position

    # Are we out of points?
    if len(available_highlights) < 1:
      return None

def draw_worm_highlights(positions:List[Position], params:LongWormParams):
  open_group("stroke=\"blue\"")

  start = positions[0]
  end = positions[-1]

  # Draw rings
  if params.draw_highlight:
    draw_ring_of_circles(params.highlight_end_points, start.x, start.y, params.highlight_end_circle_radius, params.highlight_end_point_radius)
    draw_sunburst(params.highlight_end_points, end.x, end.y, params.highlight_end_circle_radius, 10)
    # draw_ring_of_circles(params.highlight_end_points, end.x, end.y, params.highlight_end_circle_radius, params.highlight_end_point_radius)

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
    point = pick_valid_highlight(available_highlights, consumed_highlights, positions, params)
    if point is None:
      return # Ran out of points

    num = 0
    if rand_int(0, 3) == 0:
      num = rand_int(200, 50000)

    # Pick random highlight type
    highlight_index = rand_int(0, int(HighlightType.End - 1))
    highlight_type = HighlightType(highlight_index)

    highlight_count -= 1
    highlight_size = point.size + params.highlight_padding

    if params.draw_highlight:
      if connect_next:
        draw_path("M {} {} L{} {}".format(last.x, last.y, point.x, point.y))

      if highlight_type == HighlightType.Circle:
        draw_circ(point.x, point.y, highlight_size)
      elif highlight_type == HighlightType.DoubleRing:
        draw_circ(point.x, point.y, highlight_size)
        draw_circ(point.x, point.y, highlight_size + 10)
      elif highlight_type == HighlightType.SunRing:
        draw_circ(point.x, point.y, highlight_size)
        draw_sunburst(20, point.x, point.y, highlight_size + 10, 10)

      if num > 0:
        open_group("transform=\"translate({},{}) scale(0.5,0.5)\""
          .format(point.x + highlight_size * 1.5, point.y))
        draw_text(0, 0, 10, str(num))
        close_group()

    last = point
    connect_next = rand_int(0, 3) == 0

  close_group()

def draw_long_worm(params:LongWormParams):
  # Variables
  peaks = params.peaks.rand()
  top_first = rand_int(0, 1) == 0

  # Build outline
  padding = 100
  top = svg_safe().y + padding
  bottom = svg_safe().bottom() - padding
  center_y = svg_full().center_y()
  left = svg_safe().x + padding
  right = svg_safe().right() - padding
  width = right - left

  # Subdivide space
  space = width / (peaks + 1)

  # Pick direction of motion
  if top_first:
    first = top
    second = bottom
  else:
    first = bottom
    second = top

  # Pick rough points
  rough_points: List[Point] = []
  rough_points.append(Point(left, center_y))
  for i in range(0, peaks):
    rough_points.append(Point(left + space * (i + 1), first))
    rough_points.append(Point(left + space * (i + 1), second))
  rough_points.append(Point(right, center_y))

  # Shuffle rough points
  shuffle_points(params.shuffle_large_max_x, params.shuffle_large_max_y, rough_points)

  # Draw rough points
  # draw_point_path(rough_points)

  # Subdivide rough path
  points = subdivide_point_path(rough_points, params.rough_subdivisions)

  # Shuffle subdivided path
  shuffle_points(params.shuffle_small_max_x, params.shuffle_small_max_y, points)

  # Draw subdivided points
  # draw_point_path(points)

  centers = generate_centerpoints(points)
  # draw_curved_path(points, centers)
  positions = generate_final_positions(points, centers, params.size_end, params.size_min, params.size_max, params.step_dist)

  # Draw actual items created in last loop
  if params.draw_worm:
    for pos in positions:
      if params.circle:
        draw_circ(pos.x, pos.y, pos.size)
      else:
        draw_rect(pos.x - pos.size, pos.y - pos.size, pos.size * 2, pos.size * 2)

  draw_worm_highlights(positions, params)
