from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from lib_maze import *
from enum import Enum
from typing import List

###
### Infinite Maze
###

class DrawType(Enum):
  straight = 0
  curved = 1
  hatched = 2


class MazeParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.debug_draw_boundary: bool = True
    self.debug_push: bool = False
    self.draw_type: DrawType = DrawType.curved
    self.close_path: bool = True
    self.cell_size: int = 5
    self.do_cap: bool = False
    self.cap_percent: RangeFloat = RangeFloat(.8, .99)
    self.do_push: bool = False
    self.random_push: bool = False
    self.push_pad_range_max: float = .25
    self.push_pad_range_offset: float = .15
    self.push_num: RangeInt = RangeInt(800, 2000)
    self.push_range: RangeFloat = RangeFloat(400, 800)
    self.push_strength: RangeFloat = RangeFloat(0.5, 2.5) # TODOML scale?
    self.push_line_cell_size: RangeFloat = RangeFloat(100, 200)
    self.push_line_step_size = 10
    self.cutout_range = .1
    self.do_inset = False
    self.draw_cutout = True
    self.circle_inset = 15

    super().__init__(defaults)


def draw_maze(params: MazeParams, group: Group = None):
  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  cell_size = params.cell_size
  print("Cell size:", cell_size)

  # Make maze
  maze_size = MazeSize(cell_size, pad, params.cutout_range)
  maze_options = MazeOptions(
    maze_size,
    params.close_path,
    params.do_inset,
  )
  line = make_maze_line(maze_options)

  if len(line) < 1:
    print('0 length maze')
    return

  cap_index = floor(len(line) * params.cap_percent.rand())
  if params.do_cap:
    del line[cap_index: len(line)]

  print("Points:", len(line))

  # Do push
  push_params = PushParams(
    pad,
    params.debug_draw_boundary,
    params.do_push,
    params.random_push,
    params.push_pad_range_max,
    params.push_pad_range_offset,
    params.push_num,
    params.push_line_cell_size,
    params.push_line_step_size,
    params.push_range,
    params.push_strength,
  )
  push_rect = push_line(line, push_params, params.draw)

  # Scale output to fit safe area
  expand = ExpandingVolume()
  for point in line:
    expand.add(point)
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)

  # Draw the line
  scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)
  if params.debug_draw_boundary:
    if params.do_push:
      draw_rect_rect(push_rect, scaled)
      draw_circ(push_rect.x, push_rect.y, 10, scaled)
    draw_rect_rect(pad, scaled)
  if params.draw:
    if params.draw_type == DrawType.curved:
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, scaled)
    if params.draw_type == DrawType.straight:
      draw_point_path(line, scaled)
    if params.draw_type == DrawType.hatched:
      centers = generate_centerpoints(line)
      final = generate_final_points(line, centers, 1)
      draw_point_path_hatched(final, HatchParams(RangeInt(3, 10), RangeInt(1, 3)))

    if params.draw_cutout and maze_size.range_stamp > 0:
      center_x = pad.center_x()
      if maze_size.col % 2 == 0:
        center_x += maze_size.node_w
      center_y = pad.center_y()
      if maze_size.row % 2 == 0:
        center_y += maze_size.node_h

      circ_size_base = (maze_size.range_stamp * 2) * maze_size.node_w
      draw_circ(center_x, center_y, circ_size_base - params.circle_inset - (maze_size.node_w), scaled)
      draw_circ(center_x, center_y, circ_size_base - params.circle_inset - (maze_size.node_w * 2), scaled)

  close_group()
