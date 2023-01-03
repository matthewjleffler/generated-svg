import lib
import math
import random
import path
from typing import List
from enum import IntEnum

# TODO wiggle the origins

class BorderType(IntEnum):
  Empty = 0
  Circles = 1
  Starburst = 2

  End = 3

rotate_range = math.pi / 10
ring_pad = 5

def point(center_x:float, center_y:float, rad:float, dist:float) -> lib.Point:
  return lib.Point(round(cos(center_x, rad, dist), 2),
                   round(sin(center_y, rad, dist), 2))

def cos(center:float, rads:float, dist:float) -> float:
  return center + math.cos(rads) * dist

def sin(center:float, rads:float, dist:float) -> float:
  return center + math.sin(rads) * dist

def draw_circle(x:float, y:float, rays:int, min_dist:float, max_dist:float, points:List[lib.Point]):
  # Create original rough line
  rough_points: List[lib.Point] = []
  rough_points.append(point(x, y, 0, min_dist))
  rough_points.append(point(x, y, 0, max_dist))

  # Draw rough line
  # path.draw_point_circles(rough_points)
  # path.draw_point_path(rough_points)

  # Subdivide
  subdivisions = math.floor(max_dist / 10)
  if subdivisions % 2 == 1:
    subdivisions += 1
  subdivided = path.subdivide_point_path(rough_points, subdivisions, subdivisions, False)

  # Adjust control points
  for i in range(1, len(subdivided), 2):
    sub = subdivided[i].subtract_floats(x, y)
    rot = lib.rand_float(-rotate_range, rotate_range)
    fine = sub.rotate(rot)
    subdivided[i] = lib.Point(x + fine.x, y + fine.y)

  # Draw subdivided line
  # path.draw_point_circles(subdivided)
  # path.draw_point_path(subdivided)

  # Copy by number of rays
  for i in range(0, rays):
    final: List[lib.Point] = []

    rot = (i / rays) * math.pi * 2
    for sub in subdivided:
      rotated = sub.subtract_floats(x, y)
      rotated = rotated.rotate(rot)
      final.append(lib.Point(x + rotated.x, y + rotated.y))

    # Draw rotated lines
    # path.draw_point_circles(final)
    # path.draw_point_path(final)
    points.append(final)

  # points.append(subdivided)


def add_border(x, y, size_h, draw):
  ring_count = random.randint(0, 3)
  if draw:
    for i in range(0, ring_count):
      lib.circ(x, y, size_h + ring_pad + ring_pad * i)

  ring_buffer = ring_pad + ring_pad * (ring_count + 1)

  border_index = random.randint(0, int(BorderType.End) - 1)
  border = BorderType(border_index)
  if border == BorderType.Empty or not draw:
    return
  elif border == BorderType.Circles:
    lib.ring_of_circles(math.floor(size_h / 3), x, y, size_h + ring_buffer, 5)
  elif border == BorderType.Starburst:
    lib.sunburst(math.floor(size_h / 3), x, y, size_h + ring_buffer, 5)


def loop(draw_circles, draw_border):
  # lib.border()

  # Rough path
  padding = 0
  top = lib.svg_safe.y + padding
  bottom = lib.svg_safe.bottom() - padding
  height = bottom - top
  c_y = lib.svg_full.h / 2
  left = lib.svg_safe.x + padding
  right = lib.svg_safe.right() - padding
  width = right - left
  c_x = lib.svg_full.w / 2

  # Generate points and control points
  points: List[List[lib.Point]] = []

  size_h = random.randint(40, 280)
  size = size_h + 35
  size_d = size * 2

  col_max = math.floor(width / size_d)
  row_max = math.floor(height / size_d)

  offset_x = (lib.svg_safe.w - (col_max * size_d)) / 2
  offset_y = (lib.svg_safe.h - size / 2 - (row_max * size_d * .85)) / 2

  # Calculate circles and draw borders
  lib.open_group("stroke=\"blue\"")
  for row in range(0, row_max):
    y = offset_y + top + size + (size_d * .85) * row
    for col in range(0, col_max):
      x = offset_x + left + size + size_d * col
      if row % 2 == 1:
        if col == col_max - 1:
          continue
        x += size
      draw_circle(x, y, math.floor(size_h / 2), 10, size_h, points)
      add_border(x, y, size_h, draw_border)
  lib.close_group()

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
    if draw_circles:
      lib.path(path)


def loop_combined():
  loop(True, True)

def loop_circles():
  loop(True, False)

def loop_highlights():
  loop(False, True)

seed = 0
test = True
size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  lib.main("spiral-combined", test, seed, size, loop_combined)
  lib.main("spiral-circles", test, seed, size, loop_circles)
  lib.main("spiral-highlights", test, seed, size, loop_highlights)

