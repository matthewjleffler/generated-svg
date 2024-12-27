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
    self.do_cap: bool = True
    self.cap_percent: RangeFloat = RangeFloat(.8, .99)
    self.do_push: bool = True
    self.debug_push: bool = False
    self.allow_pull: bool = False
    self.push_num: RangeInt = RangeInt(1, 100)
    self.push_range: RangeFloat = RangeFloat(500, 1000)
    self.push_strength: RangeFloat = RangeFloat(5, 10) # TODOML scale?
    self.push_cap: float = 1

    super().__init__(defaults)


class Pusher:
  def __init__(self, valid: Rect, params: MazeParams):
    self.origin = Point(RangeFloat(valid.x, valid.right()).rand(), RangeFloat(valid.y, valid.bottom()).rand())
    if RangeInt(0, 1).rand() == 0 and params.allow_pull:
      self.scale = -1
    else:
      self.scale = 1
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

  if params.do_cap:
    cap_index = floor(len(line) * params.cap_percent.rand())
    del line[cap_index: len(line)]

  # Do push randomization independent of draw
  num_pushers = params.push_num.rand()
  pushers: List[Pusher] = []
  for _ in range(0, num_pushers):
    pushers.append(Pusher(pad, params))

  if params.do_push:
    for push in pushers:
      if params.debug_push:
        push.draw_debug()
      for point in line:
        delta = point.subtract_copy(push.origin)
        delta_len = delta.length()
        if delta_len > push.range:
          continue
        t = 1 - (delta_len / push.range)
        t = min(t, params.push_cap)
        push_amount = ease_in_out_quad(t, 0, push.strength, 1.5)
        if push.scale < 0:
          push_amount = min(push_amount, delta_len)
        point.add(delta.normalize().multiply(push_amount * push.scale))

  # Scale output to fit safe area
  min_x = pad.right()
  min_y = pad.bottom()
  max_x = 0
  max_y = 0
  for point in line:
    min_x = min(point.x, min_x)
    min_y = min(point.y, min_y)
    max_x = max(point.x, max_x)
    max_y = max(point.y, max_y)
  real_w = max_x - min_x
  real_h = max_y - min_y
  scale_x = pad.w / real_w
  scale_y = pad.h / real_h
  final_scale = min(scale_x, scale_y)

  final_w = real_w * final_scale
  final_h = real_h * final_scale
  offset_x = (pad.x - (min_x * scale_x) + (pad.w - final_w) / 2)
  offset_y = (pad.y - (min_y * scale_y) + (pad.h - final_h) / 2)

  # Draw the line
  scaled = open_group(GroupSettings(translate=(offset_x, offset_y), scale=final_scale), group)
  if params.draw:
    if params.draw_curved:
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, scaled)
    else:
      draw_point_path(line, scaled)
  close_group()
