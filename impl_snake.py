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
    self.draw_head: bool = False
    self.draw_ribs: bool = True
    self.draw_spine: bool = True
    self.cell_size: RangeInt = RangeInt(50, 250)
    self.do_shuffle: bool = False
    self.shuffle: RangeFloat = RangeFloat(.1, .75)
    self.do_push: bool = True
    self.random_push: bool = False,
    self.push_pad_range_max: float = .25
    self.push_num: RangeInt = RangeInt(800, 2000)
    self.push_range: RangeFloat = RangeFloat(400, 800)
    self.push_strength: RangeFloat = RangeFloat(0.5, 2.5)
    self.push_line_cell_size: RangeFloat = RangeFloat(100, 200)
    self.push_line_step_size = 10
    self.step_dist: int = 2 # 3
    self.min_dist: int = 1
    self.do_inflate: bool = True
    self.inflate_factor: float = 1.2
    self.dot_threshhold: float = -.9
    self.end_falloff: float = .02
    self.do_rib_shuffle: bool = True
    self.rib_shuffle_amount: float = .1
    self.smoothing_range: int = 60
    self.smoothing_steps: int = 3 # 10
    self.close_path: bool = False
    self.do_average: bool = True
    self.do_inflate_corners: bool = True
    self.inflate_corner_factor: float = .5
    self.do_final_average: bool = True
    self.final_average_weight: int = 2

    super().__init__(defaults)


def draw_snake(params: SnakeParams, group: Group = None):
  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  cell_size = params.cell_size.rand()
  print("Cell size:", cell_size)

  maze_size = MazeSize(cell_size, pad)
  inflate_step = max(int(min(maze_size.half_w / 2, maze_size.half_h / 2)), 5)

  # Set up params to run randomness before generating maze
  snake_params = SnakeDrawParams(
    params.draw_spine,
    params.draw_head,
    params.draw_ribs,
    params.step_dist,
    params.do_inflate,
    params.inflate_factor,
    inflate_step,
    params.end_falloff,
    params.do_average,
    params.smoothing_range,
    params.smoothing_steps,
    params.do_inflate_corners,
    params.inflate_corner_factor,
    params.do_final_average,
    params.final_average_weight,
    params.do_rib_shuffle,
    params.rib_shuffle_amount,
  )

  # Make maze
  line: List[Point] = make_maze_line(maze_size, params.close_path)
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
  push_params = PushParams(
    pad,
    params.debug_draw_boundary,
    params.do_push,
    params.random_push,
    params.push_pad_range_max,
    params.push_num,
    params.push_line_cell_size,
    params.push_line_step_size,
    params.push_range,
    params.push_strength,
  )
  push_rect = push_line(line, push_params, group)

  # Debug draw the line
  # draw_point_path(line)
  # # centers = generate_centerpoints(line)
  # # draw_curved_path(line, centers, group)
  # return

  draw_snake_from_points(line, snake_params, pad, group)

