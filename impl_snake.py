from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from lib_maze import *
from lib_snake import *
from typing import List

###
### Snake Bones
###

###
### Space filling curve algorithm based on:
### https://observablehq.com/@esperanc/random-space-filling-curves
###

class SnakeParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.debug_draw_boundary: bool = True
    self.cell_size: RangeInt = RangeInt(50, 100)
    self.do_shuffle: bool = False
    self.shuffle: RangeFloat = RangeFloat(.1, .75)

    # SnakeOptions
    self.draw_spine: bool = True
    self.draw_head: bool = False
    self.draw_ribs: bool = True
    # 3 for sharpie pens, 4 (3.5?) for 0.5 isograph
    self.step_dist: float = 3.5
    self.do_inflate: bool = True
    self.inflate_factor: float = 1.2
    self.end_falloff: float = .02
    self.do_average: bool = True
    self.smoothing_range: int = 60
    self.smoothing_steps: int = 3
    self.do_inflate_corners: bool = True
    self.inflate_corner_factor: float = .5
    self.do_final_average: bool = True
    self.final_average_weight: int = 2
    self.do_rib_shuffle: bool = True
    self.rib_shuffle_amount: float = .1

    # MazeOptions
    self.close_path: bool = False
    self.do_inset: bool = False

    # PushOptions
    self.do_push: bool = True
    self.random_push: bool = False,
    self.push_pad_range_max: float = .1
    self.push_pad_range_offset: float = .3
    self.push_num: RangeInt = RangeInt(800, 2000)
    self.push_range: RangeFloat = RangeFloat(400, 800)
    self.push_strength: RangeFloat = RangeFloat(0.5, 2.5)
    self.push_line_cell_size: RangeFloat = RangeFloat(100, 200)
    self.push_line_step_size = 15

    super().__init__(defaults)


def draw_snake(params: SnakeParams, group: Group = None):
  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  cell_size = params.cell_size.rand()
  print("Cell size:", cell_size)

  maze_size = MazeSize(cell_size, pad)

  # Make maze
  line: List[Point] = make_maze_line(maze_size, params)
  if len(line) < 1:
    print('0 length maze')
    return

  # Shuffle points
  if params.do_shuffle:
    line_len = len(line)
    for i in range(0, line_len):
      # Shuffle the individual points
      if params.close_path and (i <= 1 or i >= line_len - 2):
        continue
      line[i].add_floats(params.shuffle.rand() * maze_size.half_w, params.shuffle.rand() * maze_size.half_h)

  # Do push
  push_rect = push_line(line, pad, params, group)
  if not params.debug_draw_boundary or not params.do_push:
    push_rect = None

  # Debug draw the line
  # draw_point_path(line)
  # # centers = generate_centerpoints(line)
  # # draw_curved_path(line, centers, group)
  # return

  inflate_step = max(int(min(maze_size.half_w / 2, maze_size.half_h / 2)), 5)
  draw_snake_from_points(line, params, inflate_step, pad, push_rect, group)

