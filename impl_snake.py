from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from lib_maze import *
from lib_snake import *
from lib_triangle import *
from lib_node import *
from typing import List
from enum import Enum

###
### Snake Bones
###

###
### Space filling curve algorithm based on:
### https://observablehq.com/@esperanc/random-space-filling-curves
###

class _SnakeType(Enum):
  maze = 0
  triangle = 1

class SnakeParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.debug_draw_boundary: bool = True
    self.cell_size = 120
    self.do_shuffle: bool = True
    self.shuffle: RangeFloat = RangeFloat(0, .5)
    self.line_type: _SnakeType = _SnakeType.maze

    # SnakeOptions
    self.draw_spine: bool = True
    self.draw_head: bool = False
    self.draw_ribs: bool = True
    # 3 for sharpie pens, 4 (3.5?) for 0.5 isograph
    self.step_dist: float = 2
    self.do_inflate: bool = False
    self.inflate_factor: float = 1
    self.end_falloff: float = .02
    self.do_average: bool = True
    self.smoothing_range: int = 60
    self.smoothing_steps: int = 2
    self.do_inflate_corners: bool = True
    self.inflate_corner_factor: float = 1.1
    self.do_final_average: bool = False
    self.final_average_weight: int = 2
    self.do_rib_shuffle: bool = True
    self.raw_shuffle_amount: RangeFloat = RangeFloat(.05, .2)
    self.break_count: int = 0
    self.original_ribs: bool = False
    self.rib_range: RangeInt = RangeInt(3, 10)


    # MazeOptions
    self.close_path: bool = False
    self.do_inset: bool = False

    # PushOptions
    self.do_push: bool = False
    self.random_push: bool = False,
    self.push_pad_range_max: float = .25
    self.push_pad_range_offset: float = 0
    self.push_num: RangeInt = RangeInt(800, 2000)
    self.push_range: RangeFloat = RangeFloat(400, 800)
    self.push_strength: RangeFloat = RangeFloat(0.5, 2.5)
    self.push_line_cell_size: RangeFloat = RangeFloat(100, 200)
    self.push_line_step_size = 15

    # TriangleOptions
    self.triangle_step_size = 100

    super().__init__(defaults)


def draw_snake(params: SnakeParams, group: Group):
  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  if params.line_type == _SnakeType.maze:
    maze_size = MazeSize(params.cell_size, pad)

    # Make maze
    line: List[Point] = make_maze_line(maze_size, params)
    if len(line) < 1:
      print('0 length maze')
      return
    inflate_step = max(int(min(maze_size.half_w / 2, maze_size.half_h / 2)), 5)
  elif params.line_type == _SnakeType.triangle:
    triangle_result = create_triangle_lines(pad, params)
    line = triangle_result.triangle_points
    inflate_step = max(int(params.triangle_step_size / 4), 5)

  # Shuffle points
  if params.do_shuffle:
    line_len = len(line)
    for i in range(0, line_len):
      # Shuffle the individual points
      if params.close_path and (i <= 1 or i >= line_len - 2):
        continue
      line[i].add_floats(params.shuffle.rand() * maze_size.half_w, params.shuffle.rand() * maze_size.half_h)

  # Debug draw the line
  # draw_point_path(line)
  # # centers = generate_centerpoints(line)
  # # draw_curved_path(line, centers, group)
  # return

  snake_points = draw_snake_from_points(line, params, inflate_step)

  # Do push
  push_rect = push_lines(snake_points, pad, params, group)
  if not params.debug_draw_boundary or not params.do_push:
    push_rect = None

  # Expand Boundary
  print_overwrite("Checking volume...")
  expand = ExpandingVolume()
  expand.add_lists(snake_points)

  # Calculate scale
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)
  root_node = Node()
  root_node.transform.translate_point(offset)
  root_node.transform.scale(final_scale, final_scale)
  scaled_node = root_node.add_child()
  scaled_transform = scaled_node.transformation()
  scaled_points = scaled_transform.apply_to_point_arrays(snake_points)

  draw_boundary = try_get(params, 'debug_draw_boundary', False)
  if draw_boundary:
    group_red = get_or_create_group(GroupSettings(stroke=GroupColor.red, name="debug_red"))
    if push_rect:
      draw_rect_rect(push_rect, group)

  # Draw Result
  if params.draw_spine:
    if params.draw_head:
      head_point = snake_points[0][0]
      draw_circ(head_point.x, head_point.y, 20, group)

  break_count = try_get(params, 'break_count', 0)
  break_loop = try_get(params, 'break_loop', 3)
  break_size = 5
  break_pos = Point(break_size + 2, svg_full().bottom() - break_size - 2)
  count_breaks = 0

  if params.draw_ribs:
    len_ribs = len(scaled_points)
    for i in range(0, len_ribs):
      print_overwrite(f"Drawing rib {pad_max(i + 1, len_ribs)}")
      rib = scaled_points[i]
      centers = generate_centerpoints(rib)
      draw_curved_path(rib, centers, group)

      if i > 0 and break_count > 0 and i % break_count == 0:
        count_breaks += 1
        for i in range(0, break_loop):
          draw_circ_point(break_pos, break_size, group)
        if draw_boundary:
          draw_circ_point(rib[0], 10, group_red)

  print_finish_overwite()

  if break_count > 0 and count_breaks > 0:
    print('Breaks:', count_breaks)

  print("Finished snake")

