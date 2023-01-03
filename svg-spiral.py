import lib
import math
import random
import path
from typing import List

# TODO different borders
# TODO wiggle the origins

rotate_range = math.pi / 30
subdivisions = 20

def point(center_x:float, center_y:float, rad:float, dist:float) -> lib.Point:
  return lib.Point(round(cos(center_x, rad, dist), 2),
                   round(sin(center_y, rad, dist), 2))

def cos(center:float, rads:float, dist:float) -> float:
  return center + math.cos(rads) * dist

def sin(center:float, rads:float, dist:float) -> float:
  return center + math.sin(rads) * dist

def draw_circle(x, y, rays, min_dist, max_dist, points):
  for i in range(0, rays):
    rough_points: List[lib.Point] = []
    t = i / rays
    rad = t * math.pi * 2
    rough_points.append(point(x, y, rad, min_dist))
    rough_points.append(point(x, y, rad, max_dist))

    # Draw rough line
    # path.draw_point_circles(rough_points)
    # path.draw_point_path(rough_points)

    # Subdivide
    fine_points = path.subdivide_point_path(rough_points, subdivisions, subdivisions, False)

    # Adjust control points
    for j in range(1, len(fine_points), 2):
      fine = fine_points[j].subtract_floats(x, y)
      rotation = lib.rand_float(-rotate_range, rotate_range)
      fine = fine.rotate(rotation)
      fine_points[j] = lib.Point(x + fine.x, y + fine.y)

    # Add final content to render list
    points.append(fine_points)

    # Draw fine line
    # path.draw_point_circles(fine_points)
    # path.draw_point_path(fine_points)


def loop():
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

  size_h = random.randint(80, 120)
  size = size_h + 5
  size_d = size * 2

  col_max = math.floor(width / size_d)
  row_max = math.floor(height / size_d)

  offset_x = (lib.svg_safe.w - (col_max * size_d)) / 2
  offset_y = (lib.svg_safe.h - size / 2 - (row_max * size_d * .85)) / 2

  for row in range(0, row_max):
    y = offset_y + top + size + (size_d * .85) * row
    for col in range(0, col_max):
      x = offset_x + left + size + size_d * col
      if row % 2 == 1:
        if col == col_max - 1:
          continue
        x += size
      draw_circle(x, y, size_h, 10, size_h, points)
      lib.circ(x, y, size_h)

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

