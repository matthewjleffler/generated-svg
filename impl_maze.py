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
    self.draw_boundary_debug: bool = False
    self.draw_type: DrawType = DrawType.curved
    self.close_path: bool = True
    self.cell_size: int = 20
    self.do_cap: bool = False
    self.cap_percent: RangeFloat = RangeFloat(.8, .99)
    self.do_push: bool = True
    self.debug_push: bool = False
    self.random_push: bool = False
    self.push_rect_pad_x: RangeFloat = RangeFloat(-100, 100)
    self.push_rect_pad_y: RangeFloat = RangeFloat(-100, 100)
    self.push_num: RangeInt = RangeInt(800, 2000)
    self.push_range: RangeFloat = RangeFloat(400, 800)
    self.push_strength: RangeFloat = RangeFloat(0.5, 2.5) # TODOML scale?
    self.push_line_cell_size: RangeFloat = RangeFloat(100, 200)
    self.push_line_step_size = 10

    super().__init__(defaults)


class Pusher:
  def __init__(self, origin: Point, valid: Rect, params: MazeParams):
    self.origin = origin
    if origin is None:
      self.origin = Point(RangeFloat(valid.x, valid.right()).rand(), RangeFloat(valid.y, valid.bottom()).rand())
    self.range = params.push_range.rand()
    self.strength = params.push_strength.rand()

  def draw_debug(self):
    draw_circ_point(self.origin, 10)
    draw_circ_point(self.origin, self.range)
    draw_point_path([self.origin, self.origin.add_floats_copy(0, self.strength)])


def draw_maze(params: MazeParams, group: Group = None):
  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.draw_boundary_debug:
    draw_border(group)

  cell_size = params.cell_size
  print("Cell size:", cell_size)

  # Make maze
  line = make_maze_line(cell_size, pad, params.close_path)

  if len(line) < 1:
    print('0 length maze')
    return

  cap_index = floor(len(line) * params.cap_percent.rand())
  if params.do_cap:
    del line[cap_index: len(line)]

  print("Points:", len(line))

  # Do push randomization independent of draw
  pushers: List[Pusher] = []
  push_rect = pad.shrink_xy_copy(params.push_rect_pad_x.rand(), params.push_rect_pad_y.rand())
  if params.random_push:
    num_pushers = params.push_num.rand()
    for _ in range(0, num_pushers):
      pushers.append(Pusher(None, push_rect, params))
  else:
    push_cell = params.push_line_cell_size.rand()
    push_line = make_maze_line(push_cell, push_rect, True)
    push_center = generate_centerpoints(push_line)
    push_divisions = generate_final_points(push_line, push_center, params.push_line_step_size)

    # Draw debug
    # new_group = open_group(GroupSettings(stroke=GroupColor.red), group)
    # draw_point_circles(push_divisions, new_group)
    # close_group()

    for point in push_divisions:
      pushers.append(Pusher(point, push_rect, params))

  # Draw push
  if params.do_push:
    push_index = 0
    print('Pushing...')
    for push in pushers:
      push_index += 1
      print_overwrite(f"Running push {push_index} / {len(pushers)} ...")
      if params.debug_push:
        push.draw_debug()
      for point in line:
        delta = point.subtract_copy(push.origin)
        delta_len = delta.length()
        if delta_len > push.range:
          continue
        t = 1 - (delta_len / push.range)
        push_amount = ease_in_out_quad(t, 0, push.strength, 1)
        point.add(delta.normalize().multiply(push_amount))

  # Scale output to fit safe area
  expand = ExpandingVolume()
  for point in line:
    expand.add(point)
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)

  # Draw the line
  scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)
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
  close_group()
