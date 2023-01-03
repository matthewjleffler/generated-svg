import lib
import math
import random
import path
from typing import List

def point(center_x:float, center_y:float, rads:float, dist:float, rand_range:float) -> lib.Point:
  final_rads = rads
  if rand_range != 0:
    rad_change = lib.rand_float(-rand_range, rand_range)
    final_rads += rad_change
  return lib.Point(round(cos(center_x, final_rads, dist), 2),
                   round(sin(center_y, final_rads, dist), 2))

def cos(center:float, rads:float, dist:float) -> float:
  return center + math.cos(rads) * dist

def sin(center:float, rads:float, dist:float) -> float:
  return center + math.sin(rads) * dist

def loop():
  # lib.border()

  # Rough path
  padding = 100
  top = lib.svg_safe.y + padding
  bottom = lib.svg_safe.bottom() - padding
  height = bottom - top
  c_y = lib.svg_full.h / 2
  left = lib.svg_safe.x + padding
  right = lib.svg_safe.right() - padding
  width = right - left
  c_x = lib.svg_full.w / 2

  # Spiral settings
  ray_count = 100
  min_dist = 50
  stack_spread = 5
  max_steps = 1 + math.floor(height / stack_spread / 3.5) * 2

  # Center point
  # lib.circ(c_x, c_y, 5)

  random_middle_range = math.pi / 60
  random_outer_range = 0

  # Generate points and control points
  points: List[List[lib.Point]] = []
  for i in range(0, ray_count):
    line_points: List[lib.Point] = []
    points.append(line_points)

    in_row = i / ray_count
    rads = in_row * math.pi * 2

    for j in range(0, max_steps):
      rand = random_middle_range
      if j % 2 == 0:
        rand = random_outer_range
      line_points.append(point(c_x, c_y, rads, min_dist + stack_spread * j, rand))


  # Draw points
  for point_array in points:
    # path.draw_point_circles(point_array)
    # path.draw_point_path(point_array)

    start = point_array[0]
    path = "M{} {}".format(start.x, start.y)
    for i in range(1, len(point_array), 2):
      control = point_array[i]
      end = point_array[i + 1]
      path += "Q{} {} {} {}".format(control.x, control.y, end.x, end.y)

    lib.path(path)


seed = 0
test = True
size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  lib.main("spiral", test, seed, size, loop)

