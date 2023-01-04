import lib
import path
import random
import math
from typing import List

def create_highlight(draw:bool, line:List[lib.Point], final:float):
  available: List[int] = []
  claimed: List[int] = []

  lib.open_group("stroke=\"blue\"")

  # Variables
  strike_min = 0
  strike_max = 10
  strike = random.randint(strike_min, strike_max)

  circles_min = 0
  circles_max = 5
  circles = random.randint(circles_min, circles_max)

  # Collect available indexes
  for i in range(1, len(line) - 1):
    available.append(i)

  # Create strikethroughs
  for _ in range(0, strike):
    i = random.randint(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if draw:
      lib.path(f"M{lib.svg_safe.x} {point.y}h{lib.svg_safe.w}")

  # Collect available indexes
  available = []
  origin = line[0]
  for i in range(1, len(line) - 1, 2):
    point = line[i]
    delta = point.x - origin.x
    if delta <= 10 or i in claimed:
      # Not available
      continue
    available.append(i)

  # Create circles
  for _ in range(0, circles):
    if len(available) < 1:
      break
    i = random.randint(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if draw:
      lib.circ(origin.x - 20, point.y, 10)

  # Create starbursts
  available = []
  for i in range(1, len(line) - 1, 2):
    point = line[i]
    delta = point.x - origin.x
    if delta >= -10 or i in claimed:
      # Not available
      continue
    available.append(i)

  # Create sunbursts
  for _ in range(0, circles):
    if len(available) < 1:
      break
    i = random.randint(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if draw:
      lib.sunburst(10, final + 20, point.y, 10, 5)

  lib.close_group()


def create_lines(draw:bool):
  pad_x = 100
  left = lib.svg_safe.x + pad_x
  right = lib.svg_safe.right() - pad_x
  width = right - left
  # skew_min = -50
  # skew_max = 50
  # skew = lib.rand_float(skew_min, skew_max)

  # Pick subdivisions, make sure it's an even number
  subdivide_min = 50
  subdivide_max = 70
  subdivide = random.randint(subdivide_min, subdivide_max)
  if subdivide % 2 == 1:
    subdivide += 1

  shuffle_range_max = 50

  space = 5
  line_count = math.floor(width / space)

  # Create first line
  rough: List[lib.Point] = []
  rough.append(lib.Point(left, lib.svg_safe.y))
  rough.append(lib.Point(left, lib.svg_safe.bottom()))

  # Draw rough line
  # path.draw_point_circles(rough)
  # path.draw_point_path(rough)

  # Subdivide
  fine = path.subdivide_point_path(rough, subdivide, subdivide, False)

  # Shuffle odd points
  for i in range(1, len(fine), 2):
    fine[i].x += lib.rand_float(-shuffle_range_max, shuffle_range_max)

  # Draw fine line
  # path.draw_point_circles(fine)
  # path.draw_point_path(fine)

  # Duplicate line
  space = width / line_count
  lines: List[List[lib.Point]] = []
  for i in range(0, line_count):
    line: List[lib.Point] = []
    lines.append(line)
    for fine_point in fine:
      point = lib.Point(fine_point.x + space * i, fine_point.y)
      line.append(point)

  # Draw curves
  for line in lines:
    point = line[0]
    path_val = f"M{point.x} {point.y}"
    for i in range(1, len(line) - 1, 2):
      control = line[i]
      point = line[i + 1]
      path_val += f"Q{control.x} {control.y} {point.x} {point.y}"
      # lib.circ(x, lib.svg_safe.y, 5)

    if draw:
      lib.path(path_val)

  return (fine, lines[-1][0].x)

def loop(draw_lines, draw_highlight):
  # lib.border()

  result = create_lines(draw_lines)
  create_highlight(draw_highlight, result[0], result[1])


def loop_combined():
  loop(True, True)

def loop_lines():
  loop(True, False)

def loop_highlight():
  loop(False, True)


seed = 0
test = True
size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = lib.main("vertical-lines-combined", test, seed, size, loop_combined)
  lib.main("vertical-lines-lines", test, mainseed, size, loop_lines)
  lib.main("vertical-lines-highlight", test, mainseed, size, loop_highlight)

