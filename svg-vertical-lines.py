from lib import *
from path import *
from math import *
from typing import List

mutate = True

def create_highlight(draw:bool, line:List[Point], final:float):
  return
  available: List[int] = []
  claimed: List[int] = []

  open_group("stroke=\"blue\"")

  # Variables
  strike_min = 0
  strike_max = 10
  strike = rand_int(strike_min, strike_max)

  circles_min = 0
  circles_max = 5
  circles = rand_int(circles_min, circles_max)

  # Collect available indexes
  for i in range(1, len(line) - 1):
    available.append(i)

  # Create strikethroughs
  for _ in range(0, strike):
    i = rand_int(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if draw:
      draw_path(f"M{_svg_safe.x} {point.y}h{_svg_safe.w}")

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
    i = rand_int(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if draw:
      draw_circ(origin.x - 20, point.y, 10)

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
    i = rand_int(0, len(available) - 1)
    index = available[i]
    available.pop(i)

    claimed.append(index)
    point = line[index]
    if draw:
      draw_sunburst(10, final + 20, point.y, 10, 5)

  close_group()


def create_lines(draw:bool):
  pad_x = 100
  pad_y = 50
  top = svg_safe().y + pad_y
  bottom = svg_safe().bottom() - pad_y
  left = svg_safe().x + pad_x
  right = svg_safe().right() - pad_x
  width = right - left
  # skew_min = -50
  # skew_max = 50
  # skew = rand_float(skew_min, skew_max)

  # Pick subdivisions, make sure it's an even number
  subdivide_min = 50
  subdivide_max = 70
  subdivide = rand_int(subdivide_min, subdivide_max)
  if subdivide % 2 == 1:
    subdivide += 1

  shuffle_range_max = 40
  shuffle_range_max_y = 5

  space = 2
  rate = space / 5
  # print(rate)
  line_count = floor(width / space)

  # Create first line
  rough: List[Point] = []
  rough.append(Point(0, top))
  rough.append(Point(0, bottom))

  # Draw rough line
  # draw_point_circles(rough)
  # draw_point_path(rough)

  # Subdivide
  fine = subdivide_point_path(rough, subdivide, subdivide, False)

  # Shuffle odd points
  for i in range(1, len(fine), 2):
    fine_point = fine[i]
    fine_point.x += rand_float(-shuffle_range_max, shuffle_range_max)
    fine_point.y += rand_float(-shuffle_range_max_y, shuffle_range_max_y)

  # Draw fine line
  # draw_point_circles(fine)
  # draw_point_path(fine)

  # Duplicate line
  mutate_range_x = 3 * rate
  mutate_range_y = 3 * rate
  max_range = 30

  space = width / line_count
  lines: List[List[Point]] = []
  for i in range(0, line_count):
    line: List[Point] = []
    lines.append(line)
    for j in range(0, len(fine)):
      fine_point = fine[j]
      point = Point(round(left + fine_point.x + space * i, 2), round(fine_point.y, 2))
      line.append(point)

      if mutate:
        if j % 2 == 1:
          mutate_amt_x = rand_float(-mutate_range_x, mutate_range_x)
          fine_point.x = clamp(fine_point.x + mutate_amt_x, -max_range, max_range)

        mutate_amt_y = rand_float(-mutate_range_y, mutate_range_y)
        fine_point.y = clamp(fine_point.y + mutate_amt_y, top, bottom)

  # Draw curves
  curve = True

  for j in range(0, len(lines)):
    line = lines[j]

    if j % 2 == 0:
      point = line[0]
      path_val = f"M{point.x} {point.y}"

      if curve:
        for i in range(1, len(line) - 1, 2):
          control = line[i]
          point = line[i + 1]
          path_val += f"Q{control.x} {control.y} {point.x} {point.y}"
      else:
        for i in range(1, len(line)):
          point = line[i]
          path_val += f"L{point.x} {point.y}"

    else:
      point = line[-1]
      path_val = f"M{point.x} {point.y}"

      if curve:
        for i in range(len(line) - 2, 0, -2):
          control = line[i]
          point = line[i - 1]
          path_val += f"Q{control.x} {control.y} {point.x} {point.y}"
      else:
        for i in range(len(line) - 1, 0):
          point = line[i]
          path_val += f"L{point.x} {point.y}"

    if draw:
      # pass
      draw_path(path_val)

  return (fine, lines[-1][0].x)

def loop(draw_lines, draw_highlight):
  # draw_border()

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
size = SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = main("vertical-lines-combined", test, seed, size, loop_combined)
  main("vertical-lines-lines", test, mainseed, size, loop_lines)
  main("vertical-lines-highlight", test, mainseed, size, loop_highlight)

