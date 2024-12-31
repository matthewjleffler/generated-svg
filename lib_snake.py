from lib_math import *
from lib_path import *
from typing import List

class _SnakeNode:
  def __init__(self, point: Point, index: int, width: float) -> None:
    self.point = point
    self.index = index
    self.size = width
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
  def __init__(self, points: List[Point], centers: List[Point]) -> None:
    self.list: List[_SnakeNode] = []
    self.points = points
    self.centers = centers

  def add(self, point: Point, width: float) -> _SnakeNode:
    node = _SnakeNode(point, len(self.list), width)
    self.list.append(node)
    return node


class SnakeDrawParams:
  def __init__(
      self,
      draw_spine: bool,
      draw_head: bool,
      draw_ribs: bool,
      step_dist: int,
      do_inflate: bool,
      inflate_factor: float,
      inflate_step: int,
      end_falloff: float,
      do_average: bool,
      smoothing_range: float,
      smoothing_steps: int,
      do_inflate_corners: bool,
      inflate_corner_factor: float,
      do_final_average: bool,
      final_average_weight: int,
      do_rib_shuffle: bool,
      rib_shuffle_amount: float,
    ):
    self.draw_spine = draw_spine
    self.draw_head = draw_head
    self.draw_ribs = draw_ribs
    self.step_dist = step_dist
    self.do_inflate = do_inflate
    self.inflate_factor = inflate_factor
    self.inflate_step = inflate_step
    self.end_falloff = end_falloff
    self.do_average = do_average
    self.smoothing_range = smoothing_range
    self.smoothing_steps = smoothing_steps
    self.do_inflate_corners = do_inflate_corners
    self.inflate_corner_factor = inflate_corner_factor
    self.do_final_average = do_final_average
    self.final_average_weight = final_average_weight
    self.do_rib_shuffle = do_rib_shuffle
    self.rib_shuffle_amount = rib_shuffle_amount


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


def draw_snake_from_points(line: List[Point], params: SnakeDrawParams, rect: Rect, push_rect: Rect, group: Group = None):
  # Generate flowing lines
  ribs_subdivide_centers = generate_centerpoints(line)
  points = generate_final_points(line, ribs_subdivide_centers, params.step_dist)
  snake = _Snake(points, ribs_subdivide_centers)
  snake_len = len(points)
  print("Nodes:", snake_len)

  print_overwrite("Create snake...")
  for i in range(0, snake_len):
    print_overwrite(f"Snake node {pad_max(i + 1, snake_len)}")
    node = snake.add(points[i], 5)
    if i > 0:
      snake.list[i-1].set_next(node)

  # Fill dictionary for inflation
  if params.do_inflate:
    max_dist = snake_len / 5

    # Sort points into spatial map
    spatial: dict[(int, int), List[_SnakeNode]] = dict()
    for i in range(0, snake_len):
      print_overwrite(f"Sorting {pad_max(i + 1, snake_len)}")
      node = snake.list[i]
      key = (floor(node.point.x), floor(node.point.y))
      spatial_array = spatial.get(key, None)
      if spatial_array is None:
        spatial_array = []
        spatial[key] = spatial_array
      spatial_array.append(node)

    # Inflate to edge
    iteration = 0
    max_size = params.inflate_step
    calc_dict: dict[tuple[int, int], tuple[float,  float, float]] = dict()
    node_indexes = list(range(0, snake_len))
    while len(node_indexes) > 0:
      iteration += 1
      index = len(node_indexes)
      start_len = index
      while index >= 1:
        index -= 1
        i = node_indexes[index]
        node = snake.list[i]
        print_overwrite(f"Inflate {iteration} {pad_max(start_len - (index + 1), start_len)}")

        if node.done:
          node_indexes.pop(index)
          continue

        node.size += params.inflate_step * iteration
        max_size = max(max_size, node.size)
        x = floor(node.point.x)
        y = floor(node.point.y)

        pixels = _pixels_in_range(x, y, 0, max_size)
        nodes = _nodes_in_range(pixels, spatial)
        popped = False
        for other_node in nodes:
          if other_node.index == i:
            # Same node
            continue

          key = (max(i, other_node.index), min(i, other_node.index))
          (dot, delta_len) = calc_dict.get(key, (None, None))
          if dot is None:
            dot = node.final_vec.dot(other_node.final_vec)
            delta = node.point.subtract_copy(other_node.point)
            delta_len = delta.length()
            calc_dict[key] = (dot, delta_len)

          if abs(other_node.index - i) < max_dist and dot >= 0:
            # Close enough and pointing in the same direction
            continue

          if delta_len > node.size + other_node.size:
            # Too far
            continue

          # Touching, set size to dist
          other_node.done = True
          node.done = True
          if popped == False:
            node_indexes.pop(index)
            popped = True
          node.size = min(delta_len - other_node.size, node.size)

  # Increase inflated sizes by the given factor
  for i in range(0, snake_len):
    node = snake.list[i]
    print_overwrite(f"Inflate factor: {pad_max(i + 1, snake_len)}")
    node.size *= params.inflate_factor

  # Shrink ends
  falloff = floor(snake_len * params.end_falloff)
  print_overwrite("Shrinking ends...")
  for i in range(0, snake_len):
    print_overwrite(f"Shrinking end {pad_max(i + 1, snake_len)}")
    node = snake.list[i]
    percent_bot = node.index / falloff
    percent_end = (snake_len - 1 - node.index) / falloff
    percent = min(percent_bot, percent_end)
    percent = min(percent, 1)
    node.size = ease_in_out_quad(percent, 0, node.size, 1)

  # Average Sizes
  smoothing_range: int = floor(params.smoothing_range / params.step_dist)
  if params.do_average:
    print_overwrite("Averaging...")
    for s in range(0, params.smoothing_steps):
      for i in range(0, snake_len):
        print_overwrite(f"Averaging step: {pad_max(s + 1, params.smoothing_steps)} node: {pad_max(i + 1, snake_len)}")
        from_end = min(i, snake_len - 1 - i)
        steps = min(from_end, smoothing_range)
        if steps == 0:
          continue
        current = snake.list[i]
        avg_size = 0
        avg_vec = Point(0, 0)
        total_steps = steps * 2 + 1
        for j in range(-steps, steps + 1):
          node = snake.list[i + j]
          avg_size += node.size
          avg_vec.add(node.final_vec)
        current.size = avg_size / total_steps
        # Don't average corners as much
        avg_vec.add(current.final_vec)
        avg_vec.add(current.final_vec)
        current.final_vec = avg_vec.divide(total_steps + 2)

  # Increase corner sizes
  if params.do_inflate_corners:
    print_overwrite("Inflating corners...")
    for i in range(0, snake_len):
      print_overwrite(f"Inflating corner {pad_max(i + 1, snake_len)}")
      node = snake.list[i]
      dot = 1 - abs(node.vec().dot(node.final_vec))
      node.size *= (1 + (dot) * params.inflate_corner_factor)

  # One more average, sizes only
  if params.do_average:
    print_overwrite("Final average...")
    for s in range(0, params.smoothing_steps):
      for i in range(0, snake_len):
        print_overwrite(f"Final average step: {pad_max(s + 1, params.smoothing_steps)} node: {pad_max(i + 1, snake_len)}")
        from_end = min(i, snake_len - 1 - i)
        steps = min(from_end, smoothing_range)
        if steps == 0:
          continue
        current = snake.list[i]
        avg_size = 0
        total_steps = steps * 2 + 1
        for j in range(-steps, steps + 1):
          node = snake.list[i + j]
          avg_size += node.size
        current.size = avg_size / total_steps

  # Average vec back towards original
  if params.do_final_average:
    print_overwrite("Weight vectors...")
    for i in range(0, snake_len):
      print_overwrite(f"Weight {pad_max(i + 1, snake_len)}")
      node = snake.list[i]
      avg_vec = node.vec()
      for _ in range(0, params.final_average_weight):
        avg_vec.add(node.final_vec)
      node.final_vec = avg_vec.divide(params.final_average_weight + 1)

  # Create lines
  expand = ExpandingVolume()
  print_overwrite("Checking volume...")
  for i in range(0, snake_len):
    print_overwrite(f"Checking volume {pad_max(i + 1, snake_len)}")
    node = snake.list[i]
    point = node.point
    size = node.size
    perpendicular = node.final_vec.perpendicular_copy()
    line0 = Line(point, point.add_copy(perpendicular.multiply_copy(size)))
    line1 = Line(point, point.add_copy(perpendicular.multiply_copy(-size)))
    node.lines.append(line0)
    node.lines.append(line1)
    expand.add(line0.p1)
    expand.add(line1.p1)

  forward_indices = [1, 5]
  backward_indices = [2, 3]
  spine_count = RangeInt(5, 5)

  # Calculate scale
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), rect)
  scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)

  if push_rect:
    draw_rect_rect(push_rect, scaled)

  # Draw Result
  if params.draw_spine:
    if params.draw_head:
      head_point = snake.points[0]
      draw_circ(head_point.x, head_point.y, 20, scaled)
    draw_point_path(snake.points, scaled)

  if params.draw_ribs:
    print_overwrite("Drawing ribs...")
    for i in range(0, snake_len):
      print_overwrite(f"Drawing rib {pad_max(i + 1, snake_len)}")
      node = snake.list[i]
      for ribline in node.lines:
        ribs_subdivide = subdivide_point_path(ribline.points(), spine_count)

        shuffle_amount = params.rib_shuffle_amount * ribline.length()
        if not params.do_rib_shuffle:
          shuffle_amount = 0
        shuffle = node.final_vec.multiply_copy(shuffle_amount)

        for i in forward_indices:
          ribs_subdivide[i].add(shuffle)
        for i in backward_indices:
          ribs_subdivide[i].subtract(shuffle)

        ribs_subdivide_centers = generate_centerpoints(ribs_subdivide)
        draw_curved_path(ribs_subdivide, ribs_subdivide_centers, scaled)
  close_group()
  print_finish_overwite()
  print("Finished snake")
