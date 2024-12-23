from lib import *
from math import *
from lib_path import *
from typing import List
from enum import IntEnum


###
### Spiral Circle Design
###

class SpiralCircleParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw = True
    self.padding = 0
    self.spacing = 5
    self.points_per_step_ring = 50
    self.bump_range = RangeFloat(0, 0.1)
    self.bump_mult = RangeInt(2, 20)

    self._apply_params(defaults)


def draw_spiral_circle(params:SpiralCircleParams, group:Group = None):
  # draw_border(group)

  pad_rect = svg_safe().shrink_copy(params.padding)
  # draw_rect(pad_rect.x, pad_rect.y, pad_rect.w, pad_rect.h, group)

  bump_dist = params.bump_range.rand()
  bump_mult = params.bump_mult.rand()
  offset_rad = rand() * pi * 2
  print(bump_dist, bump_mult)
  c_x = pad_rect.center_x()
  c_y = pad_rect.center_y()
  count = floor(pad_rect.h / params.spacing * params.points_per_step_ring)

  dist_per_index = params.spacing / params.points_per_step_ring
  points: List[Point] = []
  for i in range(0, count):
    t = i / params.points_per_step_ring
    rad = pi * 2 * t
    dist = dist_per_index + sin((offset_rad + rad) * bump_mult) * bump_dist
    x = c_x + cos(rad) * dist * i
    y = c_y + sin(rad) * dist * i
    if not pad_rect.contains(x, y):
      break
    add_nondup_floats(x, y, points)

  # draw_point_circles(points, group)
  # draw_point_path(points, group)

  centerpoints: List[Point] = generate_centerpoints(points)
  # draw_point_circles(centerpoints, group)
  # draw_point_path(centerpoints, group)

  if params.draw:
    point = centerpoints[0]
    path = f"M{point.x} {point.y}"
    for i in range(1, len(centerpoints)):
      control = points[i]
      point = centerpoints[i]
      path += f"Q{control.x} {control.y} {point.x} {point.y}"

    draw_path(path, group)

