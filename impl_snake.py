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
    self.pad: int = 50
    self.draw_boundary_debug: bool = False
    self.draw_head: bool = True
    self.draw_ribs: bool = True
    self.draw_spine: bool = True
    self.cell_size: RangeInt = RangeInt(100, 175) # Min 50
    self.do_shuffle: bool = False
    self.shuffle: RangeFloat = RangeFloat(.1, .75)
    self.step_dist: int = 2 # 3
    self.min_dist: int = 1
    self.size_base: RangeFloat = RangeFloat(1, 1.25)
    self.size_range: RangeFloat = RangeFloat(.75, 1.8)
    self.size_divisions: RangeInt = RangeInt(10, 100)
    self.dot_threshhold: float = -.9
    self.end_falloff: float = .02
    self.do_rib_shuffle: bool = True
    self.rib_shuffle_amount: float = .1
    self.smoothing_range: int = 60
    self.smoothing_steps: int = 3 # 10
    self.close_path: bool = True
    self.do_average: bool = True
    self.do_inflate_corners: bool = True
    self.inflate_factor: float = .5
    self.do_final_average: bool = True
    self.final_average_weight: int = 2

    super().__init__(defaults)


def draw_snake(params: SnakeParams, group: Group = None):
  max_pad = svg_safe().copy()
  pad = svg_safe().shrink_copy(params.pad)

  # Draw safety border and page border
  if params.draw_boundary_debug:
    draw_border(group)
    draw_rect_rect(pad, group)
    draw_rect_rect(svg_full())

  cell_size = params.cell_size.rand()
  print("Cell size:", cell_size)

  row = floor(pad.h / cell_size)
  col = floor(pad.w / cell_size)
  row2 = row * 2
  col2 = col * 2

  node_w = pad.w / col2
  node_h = pad.h / row2
  half_w = node_w / 2
  half_h = node_h / 2

  # Set up params to run randomness before generating maze
  snake_params = SnakeDrawParams(
    params.draw_spine,
    params.draw_head,
    params.draw_ribs,
    params.step_dist,
    params.size_divisions.rand(), # Num divisions
    params.size_range,
    min(half_w, half_h) * params.size_base.rand(), # Max size
    params.end_falloff,
    params.do_average,
    params.smoothing_range,
    params.smoothing_steps,
    params.do_inflate_corners,
    params.inflate_factor,
    params.do_final_average,
    params.final_average_weight,
    params.do_rib_shuffle,
    params.rib_shuffle_amount,
  )

  # Make maze
  line: List[Point] = make_maze_line(cell_size, pad, params.close_path)
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
      line[i].add_floats(params.shuffle.rand() * half_w, params.shuffle.rand() * half_h)

  # Debug draw the line
  # draw_point_path(line)
  # # centers = generate_centerpoints(line)
  # # draw_curved_path(line, centers, group)
  # return

  draw_snake_from_points(line, snake_params, max_pad, group)

