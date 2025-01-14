from lib_math import *
from lib_path import *
from lib_maze import *
from typing import List

class _SnakeNode:
  def __init__(self, point: Point, index: int) -> None:
    self.point = point
    self.index = index
    self.left = 0
    self.right = 0
    self.next: _SnakeNode = None
    self.final_vec: Point = Point(0, 0)
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

  def add(self, point: Point) -> _SnakeNode:
    node = _SnakeNode(point, len(self.list))
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

def _test_edge_array(origin: Point, line: Line, edges: List[Line]) -> Point:
  closest_distance = maxsize
  hit: Point = None
  for edge in edges:
    intersection = line_intersection(edge, line)
    if intersection is None:
      # No intersection
      continue
    if not edge.test_point_on_line(intersection):
      # Not in segment
      continue
    line_vec = line.vec()
    int_vec = intersection.subtract_copy(origin)
    if line_vec.dot(int_vec) < 1:
      # Pointing at wrong edge
      continue
    int_vec_length = int_vec.length()
    if int_vec_length >= closest_distance:
      # Further than one we've checked
      continue
    closest_distance = int_vec_length
    hit = intersection
  return hit

#TODOML when crossing the spine
def _sample_width(
    origin: Point,
    vec: Point,
    edges: List[Line],
    center_edges: List[Line] # TODOML remove
  ) -> float:
  total_range = 60
  range_max = 2
  deg_delta = total_range / range_max
  min_delta = maxsize
  for i in range(-range_max, range_max):
    rot = deg_delta * i
    rotated = vec.rotate_copy(rot * deg_to_rad)
    line = Line(origin, rotated.add(origin))

    hit_edge = _test_edge_array(origin, line, edges)
    if hit_edge is None:
      continue

    edge_delta = origin.subtract_copy(hit_edge).length()
    if edge_delta < min_delta:
      min_delta = edge_delta

  if min_delta == maxsize:
    # Maybe original width?
    return 0

  return min_delta

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
    width = inflate_step * 2
    node = init_snake.add(init_spine[i])
    node.left = node.right = width
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

  edges: List[Line] = []
  center_edge: List[Line] = []
  edge_points: List[Point] = []
  for i in range(1, init_snake_len):
    print_overwrite(f"Init edges {pad_max(i + 1, init_snake_len)}")
    last_center = init_points[0][i - 1]
    next_center = init_points[0][i]
    last = init_points[i]
    next = init_points[i + 1]
    left = Line(last[0], next[0])
    right = Line(last[1], next[1])
    center = Line(last_center, next_center)
    edges.append(left)
    edges.append(right)
    center_edge.append(center)
    edge_points.append(left.points())
    edge_points.append(right.points())

  # Create final lines
  final_centers = generate_centerpoints(init_points[0])
  final_spine = generate_final_points(init_points[0], final_centers, params.step_dist)
  final_snake_len = len(final_spine)

  # Create final nodes
  final_snake = _Snake(final_spine)
  final_points: List[List[Point]] = [final_spine]
  for i in range(0, final_snake_len):
    print_overwrite(f"Creating final node {pad_max(i + 1, final_snake_len)}")
    node = final_snake.add(final_spine[i])
    if i > 0:
      final_snake.list[i-1].set_next(node)

  # Create rib widths
  rand_index = RangeInt(0, final_snake_len - 1).rand()
  for i in range(0, final_snake_len):
    print_overwrite(f"Finding final node width {pad_max(i + 1, final_snake_len)}")
    # if i != rand_index:
    #   continue
    node = final_snake.list[i]
    vec = node.vec()
    node.left = _sample_width(node.point, vec.perpendicular_copy().normalize().multiply(10), edges, center_edge)
    node.right = _sample_width(node.point, vec.perpendicular_copy().normalize().multiply(-10), edges, center_edge)

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
  smoothing_range: int = floor(params.smoothing_range / params.step_dist)
  if params.do_average:
    for s in range(0, params.smoothing_steps):
      for i in range(0, final_snake_len):
        print_overwrite(f"Averaging step: {pad_max(s + 1, params.smoothing_steps)} node: {pad_max(i + 1, final_snake_len)}")
        from_end = min(i, final_snake_len - 1 - i)
        steps = min(from_end, smoothing_range)
        if steps == 0:
          continue
        current = final_snake.list[i]
        avg_left = 0
        avg_right = 0
        avg_vec = Point(0, 0)
        total_steps = steps * 2 + 1
        for j in range(-steps, steps + 1):
          node = final_snake.list[i + j]
          avg_left += node.left
          avg_right += node.right
          avg_vec.add(node.final_vec)
        current.left = avg_left / total_steps
        current.right = avg_right / total_steps
        # Don't average corners as much
        avg_vec.add(current.final_vec)
        avg_vec.add(current.final_vec)
        current.final_vec = avg_vec.divide(total_steps + 2)

  # Increase corner sizes
  if params.do_inflate_corners:
    print_overwrite("Inflating corners...")
    for i in range(0, final_snake_len):
      print_overwrite(f"Inflating corner {pad_max(i + 1, final_snake_len)}")
      node = final_snake.list[i]
      dot = 1 - abs(node.vec().dot(node.final_vec))
      factor = (1 + (dot) * params.inflate_corner_factor)
      node.left *= factor
      node.right *= factor

  # One more average, sizes only
  if params.do_average:
    print_overwrite("Final average...")
    for s in range(0, params.smoothing_steps):
      for i in range(0, final_snake_len):
        print_overwrite(f"Final average step: {pad_max(s + 1, params.smoothing_steps)} node: {pad_max(i + 1, final_snake_len)}")
        from_end = min(i, final_snake_len - 1 - i)
        steps = min(from_end, smoothing_range)
        if steps == 0:
          continue
        current = final_snake.list[i]
        avg_left = 0
        avg_right = 0
        total_steps = steps * 2 + 1
        for j in range(-steps, steps + 1):
          node = final_snake.list[i + j]
          avg_left += node.left
          avg_right += node.right
        current.left = avg_left / total_steps
        current.right = avg_right / total_steps

  # Average vec back towards original
  if params.do_final_average:
    print_overwrite("Weight vectors...")
    for i in range(0, final_snake_len):
      print_overwrite(f"Weight {pad_max(i + 1, final_snake_len)}")
      node = final_snake.list[i]
      avg_vec = node.vec()
      for _ in range(0, params.final_average_weight):
        avg_vec.add(node.final_vec)
      node.final_vec = avg_vec.divide(params.final_average_weight + 1)

  # Create final rib edges
  # for i in range(0, final_snake_len):
  #   print_overwrite(f"Init volume {pad_max(i + 1, final_snake_len)}")
  #   node = final_snake.list[i]
  #   point = node.point
  #   perpendicular = node.final_vec.perpendicular_copy()
  #   final_points.append([point.copy(), point.add_copy(perpendicular.multiply_copy(node.left * params.inflate_factor))])
  #   final_points.append([point.copy(), point.add_copy(perpendicular.multiply_copy(-node.right * params.inflate_factor))])

  forward_indices = [1, 5]
  backward_indices = [2, 3]
  spine_count = RangeInt(5, 5)
  init_points: List[List[Point]] = []
  if params.draw_spine:
    init_points.append(init_snake.points)

  # Create ribs
  for i in range(0, final_snake_len):
    print_overwrite(f"Creating rib {pad_max(i + 1, final_snake_len)}")
    node = final_snake.list[i]
    point = node.point
    perpendicular = node.final_vec.perpendicular_copy()

    lines: List[Line] = [
      Line(point, point.add_copy(perpendicular.multiply_copy(node.left * params.inflate_factor))),
      Line(point, point.add_copy(perpendicular.multiply_copy(-node.right * params.inflate_factor))),
    ]

    for ribline in lines:
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
      final_points.append(ribs_subdivide)

  return final_points
