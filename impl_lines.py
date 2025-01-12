from lib import *
from lib_path import *
from lib_maze import *
from typing import List

###
### Lines
###

class LinesParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.debug_draw_boundary: bool = True

    self.separation = 3
    self.alternate_line_dir = False
    self.subdivisions = 100

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


def draw_lines(params: LinesParams, group: Group = None):
  pad = svg_safe().copy()
  pad_bottom = pad.bottom()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  sep_count = floor(pad.w / params.separation)
  sep_spread = pad.w / sep_count

  lines: List[List[Point]] = []
  for i in range(0, sep_count + 1):
    x = pad.x + i * sep_spread
    line = Line(Point(x, pad.y), Point(x, pad_bottom))
    if params.alternate_line_dir and i % 2 != 0:
      line.reverse()
    lines.append(line.points())

  # for line in lines:
  #   draw_point_path(line, group)

  subdivided: List[List[Point]] = []
  subdivision_range = RangeInt(params.subdivisions, params.subdivisions)
  for line in lines:
    sub = subdivide_point_path(line, subdivision_range)
    subdivided.append(sub)

  push_rect = push_lines(subdivided, pad, params, group)

  # Encapsulate
  expand = ExpandingVolume()
  expand.add_lists(subdivided)

  if params.draw:
    (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)
    scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)

    for line in subdivided:
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, scaled)
