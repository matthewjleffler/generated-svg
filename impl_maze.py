from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from lib_maze import *
from typing import List

###
### Infinite Maze
###

class MazeParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.draw_boundary_debug: bool = False
    self.draw_curved: bool = True
    self.close_path: bool = True
    self.cell_size: RangeInt = RangeInt(7, 7)

    super().__init__(defaults)


def draw_maze(params: MazeParams, group: Group = None):
  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.draw_boundary_debug:
    draw_border(group)

  cell = params.cell_size.rand()
  print("Cell size:", cell)

  row = floor(pad.h / cell)
  col = floor(pad.w / cell)
  row2 = row * 2
  col2 = col * 2

  node_w = pad.w / col2
  node_h = pad.h / row2
  half_w = node_w / 2
  half_h = node_h / 2

  # Make maze
  line: List[Point] = make_maze_line(
    row,
    col,
    node_w,
    node_h,
    pad.x + half_w,
    pad.y + half_h,
    params.close_path
  )

  if len(line) < 1:
    print('0 length maze')
    return

  # Debug draw the line
  if params.draw:
    if params.draw_curved:
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, group)
    else:
      draw_point_path(line)
