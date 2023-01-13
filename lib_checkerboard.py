from lib import *
from math import *

###
### Checkerboard Design
###

# TODO finish this

class CheckerboardParams:
  def __init__(self) -> None:
    self.size = 50
    self.bias_x = 135
    self.bias_y = 20


def draw_checkerboard(params:CheckerboardParams, group:Group = None):
  draw_border(group)

  count_horiz = floor(svg_safe().w / params.size)
  count_vert = floor(svg_safe().h / params.size)

  for i in range(0, count_horiz):
    path = f"M{svg_safe().x + i * params.size} {svg_safe().y}l{params.bias_x} {svg_safe().h}"
    draw_path(path, group)

  for i in range(0, count_vert):
    path = f"M{svg_safe().x} {svg_safe().y + params.size + i * params.size}l{svg_safe().w} {params.bias_y}"
    draw_path(path, group)

