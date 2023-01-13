from lib import *
from lib_path import *
from lib_text import *
from typing import List
from enum import IntEnum, Enum

###
### Worm Drawing
###


# Small Repeated Worm Pattern

class WormParams:
  def __init__(self) -> None:
    self.padding = 50
    self.stack_count = 50
    self.size_range = RangeInt(5, 100)
    self.stack_spread = 3
    self.draw_worm = True
    self.draw_innards = True
    self.fixed_size = 5


def _draw_worm_set(
  max_row:int,
  max_col:int,
  worm_size:int,
  fixed_size:float,
  params:WormParams):

  for row in range(0, max_row):
    origin_y = worm_size * row * 1.5

    for col in range(0, max_col):
      max_size = params.size_range.rand()
      origin_x = worm_size * col

      # Debug bounds
      # draw_rect(svg_safe().x + origin_x, svg_safe().y + origin_y, params.worm_size, params.worm_size)

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

        draw_circ(x, y, half)

def _draw_worm_layer(params:WormParams, fixed_size:float, group:Group = None):
  worm_size = params.stack_count * params.stack_spread * .75
  worm_row_size = worm_size * 1.55

  pad_x = svg_safe().w - params.padding
  pad_y = svg_safe().h - params.padding

  max_col = floor(pad_x / worm_size)
  max_row = floor(pad_y / worm_row_size)

  offset_x = (svg_safe().w - (max_col * worm_size)) / 2
  offset_y = (svg_safe().h - (max_row * worm_row_size)) / 2

  open_group(f"transform=\"translate({offset_x},{offset_y})\"", group)
  _draw_worm_set(max_row, max_col, worm_size, fixed_size, params)
  close_group()
  translate_x = svg_full().w - offset_x + worm_size * .1
  translate_y = offset_y + worm_size * .75
  open_group(f"transform=\"translate({translate_x},{translate_y}) scale(-1,1)\"", group)
  _draw_worm_set(max_row, max_col, worm_size, fixed_size, params)
  close_group()

def draw_worm(params:WormParams, group:Group = None):
  # draw_border()

  if params.draw_worm:
    _draw_worm_layer(params, 0, group)

  if params.draw_innards:
    open_group("stroke=\"blue\"", group)
    _draw_worm_layer(params, params.fixed_size)
    close_group()



# Long Worm Random Winding

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
    self.size_range = RangeInt(5, 60)

    # Highlights
    self.highlight_end_circle_radius = 30
    self.highlight_end_points = 10
    self.highlight_end_point_radius = 5
    self.highlight_sunburst_ray_len = 10

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

def draw_worm_highlights(positions:List[Position], params:LongWormParams, group:Group = None):
  open_group("stroke=\"blue\"", group)

  start = positions[0]
  end = positions[-1]

  # Draw rings
  if params.draw_highlight:
    draw_ring_of_circles(params.highlight_end_points, start.x, start.y, params.highlight_end_circle_radius, params.highlight_end_point_radius)
    draw_sunburst(params.highlight_end_points, end.x, end.y, params.highlight_end_circle_radius, params.highlight_sunburst_ray_len)
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
        open_group(f"transform=\"translate({point.x + highlight_size * 1.5},{point.y}) scale(0.5,0.5)\"")
        draw_text(0, 0, 10, str(num))
        close_group()

    last = point
    connect_next = rand_int(0, 3) == 0

  close_group()

def draw_long_worm(params:LongWormParams):
  # draw_border()

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
  positions = generate_final_positions(points, centers, params.size_end, params.size_range, params.step_dist)

  # Draw actual items created in last loop
  if params.draw_worm:
    for pos in positions:
      if params.circle:
        draw_circ(pos.x, pos.y, pos.size)
      else:
        draw_rect(pos.x - pos.size, pos.y - pos.size, pos.size * 2, pos.size * 2)

  draw_worm_highlights(positions, params)


# Spiral Worm Drawing

class SpiralWormBorderType(Enum):
  Empty = 0
  Sunburst = 1
  Circles = 2


class SprialWormParams:
  def __init__(self) -> None:
    self.ring_distance = 10
    self.weight_rings = [
      (0, 1), (1, 1), (2, 0.5), (3, 0.1), (4, 0.05)
    ]
    self.weight_border = [
      (SpiralWormBorderType.Empty, 1), (SpiralWormBorderType.Sunburst, 0.5), (SpiralWormBorderType.Circles, 0.5)
    ]
    self.h2_size = RangeInt(25, 100)
    self.draw_worm = True
    self.draw_highlight = True
    self.draw_highlight2 = True
    self.padding = 100
    self.spiral_rows = 4
    self.points_per_ring = 10
    self.rough_shuffle_range = 20
    self.fine_shuffle_range = 30
    self.rough_clamp_distance = 30
    self.subdivision_range = RangeInt(3, 7)
    self.position_range = RangeInt(1, 50)
    self.position_steps = 3


def _spiral_worm_highlight(
  height:float,
  x:float, y:float,
  params:SprialWormParams):

  rings = weighted_random(params.weight_rings)
  half_height = height / 2
  if params.draw_highlight:
    for i in range(0, rings):
      draw_circ(x, y, half_height + params.ring_distance * i)

  max_ring = half_height + params.ring_distance * rings
  border = weighted_random(params.weight_border)
  if params.draw_highlight:
    if border == SpiralWormBorderType.Empty:
      pass
    elif border == SpiralWormBorderType.Circles:
      draw_ring_of_circles(100, x, y, max_ring, 5)
    elif border == SpiralWormBorderType.Sunburst:
      draw_sunburst(100, x, y, max_ring, 15)


def _highlight_2(
  width:float,
  height:float,
  x:float, y:float,
  positions:List[Position],
  params:SprialWormParams):

  center = (width - height)

  size = params.h2_size.rand()
  left_rings = rand_int(1, 4)
  left_circ_x = x - center

  size = params.h2_size.rand()
  right_rings = rand_int(1, 4)
  right_circ_x = x + center

  pos_index = rand_int(0, len(positions) - 1)
  pos = positions[pos_index]
  path = "M{} {}L{} {}L{} {}".format(left_circ_x, y, pos.x, pos.y, right_circ_x, y)

  if params.draw_highlight2:
    for i in range(0, left_rings):
      draw_circ(left_circ_x, y, size + 10 * i)
    for i in range(0, right_rings):
      draw_circ(right_circ_x, y, size + 10 * i)
    draw_path(path)
    draw_circ(pos.x, pos.y, pos.size + 10)


def draw_spiral_worm(params:SprialWormParams, group:Group = None):
  # draw_border()

  # Build outline
  top = svg_safe().y + params.padding
  bottom = svg_safe().bottom() - params.padding
  height = bottom - top
  center_y = svg_full().center_y()
  left = svg_safe().x + params.padding
  right = svg_safe().right() - params.padding
  width = right - left
  center_x = svg_full().center_x()

  # Spiral settings
  spacing = height / (params.spiral_rows * 4)
  total_points = params.points_per_ring * params.spiral_rows
  rand_offset = rand() * pi * 2

  # Generate rough points
  rough_points: List[Point] = []
  for i in range(0, total_points):
    spiral = floor(i / params.points_per_ring) / params.spiral_rows
    in_row = (i % params.points_per_ring) / params.points_per_ring

    dist = spiral * params.points_per_ring * spacing + in_row * spacing * 2

    rads = in_row * pi * 2
    x = center_x + cos(rads + rand_offset) * dist
    y = center_y + sin(rads + rand_offset) * dist
    rough_points.append(Point(x, y))

  # Shuffle rough points
  shuffle_points(params.rough_shuffle_range, params.rough_shuffle_range, rough_points)

  # Draw rough points
  # draw_point_circles(rough_points, group)
  # draw_point_path(rough_points, group)

  # Subdivide path into final points
  points = subdivide_point_path(rough_points, params.subdivision_range)

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

  open_group("stroke=\"blue\"", group)
  _spiral_worm_highlight(height, center_x, center_y, params)
  close_group()

  open_group("stroke=\"red\"", group)
  _highlight_2(width, height, center_x, center_y, positions, params)
  close_group()

