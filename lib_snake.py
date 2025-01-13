from lib_math import *
from lib_path import *
from lib_maze import *
from typing import List

class _SnakeNode:
  def __init__(self, point: Point, index: int, left: float, right: float) -> None:
    self.point = point
    self.index = index
    self.left = left
    self.right = right
    self.next: _SnakeNode = None
    self.final_vec: Point = Point(0, 0)
    self.lines: List[Line] = []
    self.done = False

  def set_next(self, next: '_SnakeNode') -> None:
    self.next = next
    self.final_vec = self.vec()

  def vec(self) -> Point:
    if self.next is None:
      return Point(0, 0)
    return self.next.point.subtract_copy(self.point).normalize()


class _Snake:
  def __init__(self, points: List[Point]) -> None:
    self.list: List[_SnakeNode] = []
    self.points = points
    # self.centers = centers

  def add(self, point: Point, left: float, right: float) -> _SnakeNode:
    node = _SnakeNode(point, len(self.list), left, right)
    self.list.append(node)
    return node


class SnakeOptions:
  debug_draw_boundary: bool
  draw_spine: bool
  draw_head: bool
  draw_ribs: bool
  step_dist: float
  do_inflate: bool
  inflate_factor: float
  end_falloff: float
  do_average: bool
  smoothing_range: int
  smoothing_steps: int
  do_inflate_corners: bool
  inflate_corner_factor: float
  do_final_average: bool
  final_average_weight: int
  do_rib_shuffle: bool
  rib_shuffle_amount: float
  break_count: int
  break_loop: int


def _nodes_in_range(pixels: List[tuple[int, int]], spatial: dict[(int, int), List[_SnakeNode]]) -> List[_SnakeNode]:
  result: List[_SnakeNode] = []
  for pixel in pixels:
    nodes = spatial.get(pixel, None)
    if nodes is None:
      continue
    result += nodes
  return result


def _pixels_in_range(x: int, y: int, min: int, max: int) -> List[tuple[int, int]]:
  result: List[tuple[int, int]] = []
  for range_x in range(-max, max + 1):
    for range_y in range(-max, max + 1):
      if abs(range_x) < min or abs(range_y) < min:
        continue
      result.append((x + range_x, y + range_y))
  return result


def _find_original_index(index: int, step_dist: float, original: List[Point]) -> int:
  target = index * step_dist
  for i in range(1, len(original)):
    last = original[i - 1]
    current = original[i]
    delta = last.subtract_copy(current).length()
    target -= delta
    if target < 0:
      return i
  return len(original) - 1

def _sample_width(index: int, step_dist: float, original:List[List[Point]]) -> tuple[float, float, List[Point]]:
  original_index = _find_original_index(index, step_dist, original[0])
  original_point = original[0][original_index]
  original_ribs = original[original_index + 1]
  left = original_point.subtract_copy(original_ribs[0]).length()
  right = original_point.subtract_copy(original_ribs[1]).length()
  return (left, right, original_ribs)


def draw_snake_from_points(line: List[Point], params: SnakeOptions, inflate_step: float, rect: Rect) -> List[List[Point]]:
  # Generate flowing lines
  init_centers = generate_centerpoints(line)
  init_spine = generate_final_points(line, init_centers, 10)
  init_snake_len = len(init_spine)
  print("Init Nodes:", init_snake_len)

  # Init snake
  init_snake = _Snake(init_spine)
  for i in range(0, init_snake_len):
    print_overwrite(f"Init node {pad_max(i + 1, init_snake_len)}")
    width = inflate_step * 2 * params.inflate_factor
    node = init_snake.add(init_spine[i], width, width)
    if i > 0:
      init_snake.list[i-1].set_next(node)

  # Create Rib Edges
  init_points: List[List[Point]] = [init_spine]
  for i in range(0, init_snake_len):
    print_overwrite(f"Init volume {pad_max(i + 1, init_snake_len)}")
    node = init_snake.list[i]
    point = node.point
    perpendicular = node.final_vec.perpendicular_copy()
    init_points.append([
      point.add_copy(perpendicular.multiply_copy(node.left)),
      point.add_copy(perpendicular.multiply_copy(-node.right)),
    ])

  # Do push
  push_rect = push_lines(init_points, rect, params)
  if not params.debug_draw_boundary or not params.do_push:
    push_rect = None

  # Create final lines
  final_centers = generate_centerpoints(init_points[0])
  final_spine = generate_final_points(init_points[0], final_centers, params.step_dist)
  final_snake_len = len(final_spine)

  # Create final nodes
  final_snake = _Snake(final_spine)
  final_points: List[List[Point]] = [final_spine]
  for i in range(0, final_snake_len):
    print_overwrite(f"Final node {pad_max(i + 1, final_snake_len)}")
    (left, right, orig) = _sample_width(i, params.step_dist, init_points)

    node = final_snake.add(final_spine[i], left, right)
    final_points.append([node.point, orig[0]])
    final_points.append([node.point, orig[1]])
    if i > 0:
      final_snake.list[i-1].set_next(node)

  # Shrink ends
  falloff = floor(final_snake_len * params.end_falloff)
  for i in range(0, final_snake_len):
    print_overwrite(f"Shrinking end {pad_max(i + 1, final_snake_len)}")
    node = final_snake.list[i]
    percent_bot = node.index / falloff
    percent_end = (final_snake_len - 1 - node.index) / falloff
    percent = min(percent_bot, percent_end)
    percent = min(percent, 1)
    node.left = ease_in_out_quad(percent, 0, node.left, 1)
    node.right = ease_in_out_quad(percent, 0, node.right, 1)

  # Average Sizes
  # smoothing_range: int = floor(params.smoothing_range / params.step_dist)
  # if params.do_average:
  #   for s in range(0, params.smoothing_steps):
  #     for i in range(0, final_snake_len):
  #       print_overwrite(f"Averaging step: {pad_max(s + 1, params.smoothing_steps)} node: {pad_max(i + 1, final_snake_len)}")
  #       from_end = min(i, final_snake_len - 1 - i)
  #       steps = min(from_end, smoothing_range)
  #       if steps == 0:
  #         continue
  #       current = final_snake.list[i]
  #       avg_left = 0
  #       avg_right = 0
  #       avg_vec = Point(0, 0)
  #       total_steps = steps * 2 + 1
  #       for j in range(-steps, steps + 1):
  #         node = final_snake.list[i + j]
  #         avg_left += node.left
  #         avg_right += node.right
  #         avg_vec.add(node.final_vec)
  #       current.left = avg_left / total_steps
  #       current.right = avg_right / total_steps
  #       # Don't average corners as much
  #       avg_vec.add(current.final_vec)
  #       avg_vec.add(current.final_vec)
  #       current.final_vec = avg_vec.divide(total_steps + 2)

  # Create final rib edges
  for i in range(0, final_snake_len):
    print_overwrite(f"Init volume {pad_max(i + 1, final_snake_len)}")
    node = final_snake.list[i]
    point = node.point
    perpendicular = node.final_vec.perpendicular_copy()
    final_points.append([point.copy(), point.add_copy(perpendicular.multiply_copy(node.left))])
    final_points.append([point.copy(), point.add_copy(perpendicular.multiply_copy(-node.right))])

  return final_points + init_points

  # Increase corner sizes
  # if params.do_inflate_corners:
  #   print_overwrite("Inflating corners...")
  #   for i in range(0, snake_len):
  #     print_overwrite(f"Inflating corner {pad_max(i + 1, snake_len)}")
  #     node = snake.list[i]
  #     dot = 1 - abs(node.vec().dot(node.final_vec))
  #     node.size *= (1 + (dot) * params.inflate_corner_factor)

  # One more average, sizes only
  # if params.do_average:
  #   print_overwrite("Final average...")
  #   for s in range(0, params.smoothing_steps):
  #     for i in range(0, snake_len):
  #       print_overwrite(f"Final average step: {pad_max(s + 1, params.smoothing_steps)} node: {pad_max(i + 1, snake_len)}")
  #       from_end = min(i, snake_len - 1 - i)
  #       steps = min(from_end, smoothing_range)
  #       if steps == 0:
  #         continue
  #       current = snake.list[i]
  #       avg_size = 0
  #       total_steps = steps * 2 + 1
  #       for j in range(-steps, steps + 1):
  #         node = snake.list[i + j]
  #         avg_size += node.size
  #       current.size = avg_size / total_steps

  # Average vec back towards original
  # if params.do_final_average:
  #   print_overwrite("Weight vectors...")
  #   for i in range(0, snake_len):
  #     print_overwrite(f"Weight {pad_max(i + 1, snake_len)}")
  #     node = snake.list[i]
  #     avg_vec = node.vec()
  #     for _ in range(0, params.final_average_weight):
  #       avg_vec.add(node.final_vec)
  #     node.final_vec = avg_vec.divide(params.final_average_weight + 1)

  return final_points

  forward_indices = [1, 5]
  backward_indices = [2, 3]
  spine_count = RangeInt(5, 5)
  init_points: List[List[Point]] = []
  if params.draw_spine:
    init_points.append(init_snake.points)

  print_overwrite("Creating ribs...")
  for i in range(0, init_snake_len):
    print_overwrite(f"Creating rib {pad_max(i + 1, init_snake_len)}")
    node = init_snake.list[i]
    for ribline in node.lines:
      ribs_subdivide = subdivide_point_path(ribline.points(), spine_count)

      shuffle_amount = params.rib_shuffle_amount * ribline.length()
      if not params.do_rib_shuffle:
        shuffle_amount = 0
      shuffle = node.final_vec.multiply_copy(shuffle_amount)

      for j in forward_indices:
        ribs_subdivide[j].add(shuffle)
      for j in backward_indices:
        ribs_subdivide[j].subtract(shuffle)

      # centers = generate_centerpoints(ribs_subdivide)
      # final_rib = generate_final_points(ribs_subdivide, centers, 1)
      init_points.append(ribs_subdivide)

  return init_points
