from lib import *
from math import *
from path import *
from typing import List
from enum import IntEnum

# TODO wiggle the origins

class BorderType(IntEnum):
  Empty = 0
  Circles = 1
  Starburst = 2

rotate_range = pi / 10
ring_pad = 5

def point(center_x:float, center_y:float, rad:float, dist:float) -> Point:
  return Point(round(cos_point(center_x, rad, dist), 2),
               round(sin_point(center_y, rad, dist), 2))

def cos_point(center:float, rads:float, dist:float) -> float:
  return center + cos(rads) * dist

def sin_point(center:float, rads:float, dist:float) -> float:
  return center + sin(rads) * dist

def draw_circle(x:float, y:float, rays:int, min_dist:float, max_dist:float, points:List[Point]):
  # Create original rough line
  rough_points: List[Point] = []
  rough_points.append(point(x, y, 0, min_dist))
  rough_points.append(point(x, y, 0, max_dist))

  # Draw rough line
  # draw_point_circles(rough_points)
  # draw_point_path(rough_points)

  # Subdivide
  subdivisions = floor(max_dist / 10)
  if subdivisions % 2 == 1:
    subdivisions += 1
  subdivided = subdivide_point_path(rough_points, subdivisions, subdivisions, False)

  # Adjust control points
  for i in range(1, len(subdivided), 2):
    sub = subdivided[i].subtract_floats_copy(x, y)
    rot = rand_float(-rotate_range, rotate_range)
    fine = sub.rotate_copy(rot)
    subdivided[i] = Point(x + fine.x, y + fine.y)

  # Draw subdivided line
  # draw_point_circles(subdivided)
  # draw_point_path(subdivided)

  # Copy by number of rays
  for i in range(0, rays):
    final: List[Point] = []

    rot = (i / rays) * pi * 2
    for sub in subdivided:
      rotated = sub.subtract_floats_copy(x, y)
      rotated = rotated.rotate_copy(rot)
      final.append(Point(x + rotated.x, y + rotated.y))

    # Draw rotated lines
    # draw_point_circles(final)
    # draw_point_path(final)
    points.append(final)

  # points.append(subdivided)

ring_weights: List[tuple[int, float]] = [
  (0, 5), (1, 2), (2, 1), (3, 0.5)
]

border_weights: List[tuple[BorderType, float]] = [
  (BorderType.Empty, 5), (BorderType.Circles, 1), (BorderType.Starburst, 2)
]

def add_border(x, y, size_h, draw):
  ring_count = weighted_random(ring_weights)

  if draw:
    for i in range(0, ring_count):
      draw_circ(x, y, size_h + ring_pad + ring_pad * i)

  ring_buffer = ring_pad + ring_pad * (ring_count + 1)

  border = weighted_random(border_weights)
  if border == BorderType.Empty or not draw:
    return
  elif border == BorderType.Circles:
    draw_ring_of_circles(floor(size_h / 3), x, y, size_h + ring_buffer, 5)
  elif border == BorderType.Starburst:
    draw_sunburst(floor(size_h / 3), x, y, size_h + ring_buffer, 5)


def loop(draw_circles, border):
  draw_border()

  # Rough path
  padding = 0
  top = svg_safe().y + padding
  bottom = svg_safe().bottom() - padding
  height = bottom - top
  c_y = svg_full().center_y()
  left = svg_safe().x + padding
  right = svg_safe().right() - padding
  width = right - left
  c_x = svg_full().center_x()

  # Generate points and control points
  points: List[List[Point]] = []

  size_h = rand_int(20, 350)
  size = size_h + 20
  size_d = size * 2

  col_max = floor(width / size_d)
  row_max = floor(height / size_d)

  offset_x = (svg_safe().w - (col_max * size_d)) / 2
  offset_y = (svg_safe().h - size / 2 - (row_max * size_d * .85)) / 2

  # Calculate circles and draw borders
  open_group("stroke=\"blue\"")
  for row in range(0, row_max):
    y = offset_y + top + size + (size_d * .85) * row
    for col in range(0, col_max):
      x = offset_x + left + size + size_d * col
      if row % 2 == 1:
        if col == col_max - 1:
          continue
        x += size
      draw_circle(x, y, floor(size_h / 2), 10, size_h, points)
      add_border(x, y, size_h, border)
  close_group()

  # Draw points
  for point_array in points:
    # draw_point_circles(point_array)
    # draw_point_path(point_array)

    start = point_array[0]
    path = "M{} {}".format(start.x, start.y)
    for i in range(1, len(point_array), 2):
      control = point_array[i]
      end = point_array[i + 1]
      path += "Q{} {} {} {}".format(control.x, control.y, end.x, end.y)
    if draw_circles:
      draw_path(path)


def loop_combined():
  loop(True, True)

def loop_circles():
  loop(True, False)

def loop_highlights():
  loop(False, True)

seed = 0
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  real_seed = main("spiral-combined", test, seed, size, loop_combined)
  main("spiral-circles", test, real_seed, size, loop_circles)
  main("spiral-highlights", test, real_seed, size, loop_highlights)

