import lib
import random
import math
import path
from typing import List

def clamp_points(clamp:int, points:List[lib.Point]):
  for point in points:
    point.x = round(point.x / clamp, 0) * clamp
    point.y = round(point.y / clamp, 0) * clamp


def loop():
  # lib.border()

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

  # Scale positions towards end
  # length = len(positions)
  # for i in range(0, length):
  #   t = i / length
  #   pos = positions[i]
  #   pos.size *= max(t * 5, 1)

  # Draw results
  # round_size = 5
  # round_pos = 20

  for pos in positions:
    lib.circ(pos.x, pos.y, pos.size)

    # size = round(pos.size / round_size, 0) * round_size
    # size_2 = size * 2
    # x = round(pos.x / round_pos, 0) * round_pos
    # y = round(pos.y / round_pos, 0) * round_pos

    # lib.circ(x, y, size)
    # lib.rect(x - size, y - size, size_2, size_2)


seed = 5340805198339474029
test = False
image_size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = lib.main(
    "spiral-worm",
    test,
    seed,
    image_size,
    loop
  )
