from lib_group import *
from lib_math import Rect
from math import *


# Drawing
_round_digits = 2

def draw_rect(x:float, y:float, w:float, h:float, group:Group):
  x = round(x, _round_digits)
  y = round(y, _round_digits)
  w = round(w, _round_digits)
  h = round(h, _round_digits)
  group.children.append(f"<rect x=\"{x}\" y=\"{y}\" width=\"{w}\" height=\"{h}\"/>")

def draw_rect_rect(rect: Rect, group: Group):
  draw_rect(rect.x, rect.y, rect.w, rect.h, group)

def draw_circ(x:float, y:float, r:float, group:Group):
  x = round(x, _round_digits)
  y = round(y, _round_digits)
  r = round(r, _round_digits)
  group.children.append(f"<circle cx=\"{x}\" cy=\"{y}\" r=\"{r}\"/>")

def draw_circ_point(point: Point, r:float, group:Group):
  draw_circ(point.x, point.y, r, group)

def draw_path(value:str, group:Group):
  group.children.append(f"<path d=\"{value}\"/>")

def draw_sunburst(bursts:int, c_x:float, c_y:float, start_rad:float, ray_len:float, group:Group):
  sunburst_points = bursts
  for i in range(0, sunburst_points):
    t = i / sunburst_points
    rad = t * pi * 2

    x = c_x + sin(rad) * (start_rad)
    y = c_y + cos(rad) * (start_rad)

    vec = Point(x, y)
    vec = vec.subtract_copy(Point(c_x, c_y))
    vec.normalize()
    vec.multiply(ray_len)
    draw_path("M{} {} L{} {}".format(
      round(x, _round_digits),
      round(y, _round_digits),
      round(x + vec.x, _round_digits),
      round(y + vec.y, _round_digits)),
      group
    )

def draw_ring_of_circles(number:int, c_x:float, c_y:float, center_rad:float, circle_rad:float, group:Group):
  for i in range(0, number):
    t = i / number
    rad = t * pi * 2

    x = c_x + cos(rad) * center_rad
    y = c_y + sin(rad) * center_rad
    draw_circ(x, y, circle_rad, group)