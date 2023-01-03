import lib
import random
import math
import path
from typing import List
from enum import Enum

def clamp_points(clamp:int, points:List[lib.Point]):
  for point in points:
    point.x = round(point.x / clamp, 0) * clamp
    point.y = round(point.y / clamp, 0) * clamp


class BorderType(Enum):
  Empty = 0
  Sunburst = 1
  Circles = 2

ring_distance = 10

weight_rings: List[tuple[int, float]] = [
  (0, 1), (1, 1), (2, 0.5), (3, 0.1), (4, 0.05)
]

weight_border: List[tuple[BorderType, float]] = [
  (BorderType.Empty, 1), (BorderType.Sunburst, 0.5), (BorderType.Circles, 0.5)
]

def highlight(height, x, y, draw_highlight):
  rings = lib.weighted_random(weight_rings)
  half_height = height / 2
  if draw_highlight:
    for i in range(0, rings):
      lib.circ(x, y, half_height + ring_distance * i)

  max_ring = half_height + ring_distance * rings
  border = lib.weighted_random(weight_border)
  if draw_highlight:
    if border == BorderType.Empty:
      pass
    elif border == BorderType.Circles:
      lib.ring_of_circles(100, x, y, max_ring, 5)
    elif border == BorderType.Sunburst:
      lib.sunburst(100, x, y, max_ring, 15)


h2_size_min = 25
h2_size_max = 100

def highlight_2(width, height, x, y, draw_highlight, positions):
  center = (width - height)

  size = random.randrange(h2_size_min, h2_size_max)
  left_rings = random.randint(1, 4)
  left_circ_x = x - center

  size = random.randrange(h2_size_min, h2_size_max)
  right_rings = random.randint(1, 4)
  right_circ_x = x + center

  pos_index = random.randint(0, len(positions) - 1)
  pos = positions[pos_index]
  path = "M{} {}L{} {}L{} {}".format(left_circ_x, y, pos.x, pos.y, right_circ_x, y)

  if draw_highlight:
    for i in range(0, left_rings):
      lib.circ(left_circ_x, y, size + 10 * i)
    for i in range(0, right_rings):
      lib.circ(right_circ_x, y, size + 10 * i)
    lib.path(path)
    lib.circ(pos.x, pos.y, pos.size + 10)



def loop(draw_worm, draw_highlight, draw_highlight_2):
  lib.border()

  # Build outline
  padding = 100
  top = lib.svg_safe.y + padding
  bottom = lib.svg_safe.bottom() - padding
  height = bottom - top
  center_y = lib.svg_full.h / 2
  left = lib.svg_safe.x + padding
  right = lib.svg_safe.right() - padding
  width = right - left
  center_x = lib.svg_full.w / 2

  # Spiral settings
  spiral_rows = 4
  points_per_ring = 10
  spacing = height / (spiral_rows * 4)
  total_points = points_per_ring * spiral_rows
  rand_offset = random.random() * math.pi * 2

  # Generate rough points
  rough_points: List[lib.Point] = []
  for i in range(0, total_points):
    spiral = math.floor(i / points_per_ring) / spiral_rows
    in_row = (i % points_per_ring) / points_per_ring

    dist = spiral * points_per_ring * spacing + in_row * spacing * 2

    rads = in_row * math.pi * 2
    x = center_x + math.cos(rads + rand_offset) * dist
    y = center_y + math.sin(rads + rand_offset) * dist
    rough_points.append(lib.Point(x, y))

  # Shuffle rough points
  rough_shuffle_range = 20
  path.shuffle_points(rough_shuffle_range, rough_shuffle_range, rough_points)

  # Draw rough points
  # path.draw_point_circles(rough_points)
  # path.draw_point_path(rough_points)

  # Subdivide path into final points
  points = path.subdivide_point_path(rough_points, 3, 7)

  # Cull close points
  clamp_points(30, points)
  path.clean_duplicates(points)

  # Shuffle fine points
  fine_shuffle_range = 30
  path.shuffle_points(fine_shuffle_range, fine_shuffle_range, points)

  clamp_points(1, points)
  path.clean_duplicates(points)

  # Draw fine points
  # path.draw_point_circles(points)
  # path.draw_point_path(points)

  # Generate curve
  centers = path.generate_centerpoints(points)

  # Draw curve
  # path.draw_curved_path(points, centers)

  # Generate positions
  positions = path.generate_final_positions(points, centers, 1, 1, 50, 3)

  if draw_worm:
    for pos in positions:
      lib.circ(pos.x, pos.y, pos.size)

  lib.open_group("stroke=\"blue\"")
  highlight(height, center_x, center_y, draw_highlight)
  lib.close_group()

  lib.open_group("stroke=\"red\"")
  highlight_2(width, height, center_x, center_y, draw_highlight_2, positions)
  lib.close_group()

def loop_combined():
  loop(True, True, True)

def loop_worm():
  loop(True, False, False)

def loop_highlight():
  loop(False, True, False)

def loop_highlight_2():
  loop(False, False, True)

seed = 0
test = True
image_size = lib.SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = lib.main("spiral-worm-combined", test, seed, image_size, loop_combined)
  lib.main("spiral-worm-worm", test, mainseed, image_size, loop_worm)
  lib.main("spiral-worm-highlight", test, mainseed, image_size, loop_highlight)
  lib.main("spiral-worm-highlight-2", test, mainseed, image_size, loop_highlight_2)
