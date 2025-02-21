from lib import *


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


class SnakeOptions(TypedDict):
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
  rib_shuffle_amount: RangeFloat
  break_count: int
  break_loop: int
  original_ribs: bool
  rib_range: RangeInt


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


def draw_snake_from_points(line: List[Point], options: SnakeOptions, inflate_step: float) -> List[List[Point]]:
  reload_libs(globals())

  # Generate flowing lines
  ribs_subdivide_centers = generate_centerpoints(line)
  points = generate_final_points(line, ribs_subdivide_centers, options.get('step_dist', 100))
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
  # TODOML remove?
  if options.get('do_inflate', False):
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
    max_size = inflate_step
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

        node.size += inflate_step * iteration
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
  else:
    for i in range(0, snake_len):
      node = snake.list[i]
      print_overwrite(f"Set init size: {pad_max(i + 1, snake_len)}")
      node.size = inflate_step * 2

  # Increase inflated sizes by the given factor
  for i in range(0, snake_len):
    node = snake.list[i]
    print_overwrite(f"Inflate factor: {pad_max(i + 1, snake_len)}")
    node.size *= options.get('inflate_factor', 1)

  # Shrink ends
  falloff = floor(snake_len * options.get('end_falloff', .1))
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
  smoothing_range: int = floor(options.get('smoothing_range', 30) / options.get('step_dist'))
  smoothing_steps = options.get('smoothing_steps', 1)
  if options.get('do_average', True):
    print_overwrite("Averaging...")
    for s in range(0, smoothing_steps):
      for i in range(0, snake_len):
        print_overwrite(f"Averaging step: {pad_max(s + 1, smoothing_steps)} node: {pad_max(i + 1, snake_len)}")
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
  if options.get('do_inflate_corners', True):
    print_overwrite("Inflating corners...")
    inflate_corner_factor = options.get('inflate_corner_factor', 1.2)
    for i in range(0, snake_len):
      print_overwrite(f"Inflating corner {pad_max(i + 1, snake_len)}")
      node = snake.list[i]
      dot = 1 - abs(node.vec().dot(node.final_vec))
      node.size *= (1 + (dot) * inflate_corner_factor)

  # One more average, sizes only
  if options.get('do_average', True):
    print_overwrite("Final average...")
    for s in range(0, smoothing_steps):
      for i in range(0, snake_len):
        print_overwrite(f"Final average step: {pad_max(s + 1, smoothing_steps)} node: {pad_max(i + 1, snake_len)}")
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
  # TODOML remove this
  if options.get('do_final_average', True):
    print_overwrite("Weight vectors...")
    final_average_weight = options.get('final_average_weight', 2)
    for i in range(0, snake_len):
      print_overwrite(f"Weight {pad_max(i + 1, snake_len)}")
      node = snake.list[i]
      avg_vec = node.vec()
      for _ in range(0, final_average_weight):
        avg_vec.add(node.final_vec)
      node.final_vec = avg_vec.divide(final_average_weight + 1)

  forward_indices = []
  backward_indices = []
  rib_sub_count = RangeInt(5, 5)
  original_ribs = options.get('original_ribs', True)
  if original_ribs:
    forward_indices += [1, 5]
    backward_indices += [2, 3]
    raw_shuffle_amount = .1
  else:
    rib_range_count = options.get('rib_range', RangeInt(5, 5)).rand()
    rib_sub_count = RangeInt(rib_range_count, rib_range_count)
    rib_indexes = list(range(0, rib_range_count))
    rib_change = floor(rib_range_count / 2)
    rib_dir = RangeInt(0, 1)
    raw_shuffle_amount = options.get('rib_shuffle_amount', RangeFloat(.1, .2)).rand()
    while rib_change > 0:
      rib_change -= 1
      index = RangeInt(0, len(rib_indexes) - 1).rand()
      index = rib_indexes.pop(index)
      if rib_dir.rand() == 0:
        # Forward
        forward_indices.append(index)
      else:
        backward_indices.append(index)

  final_points: List[List[Point]] = []

  if options.get('draw_spine', True):
    final_points.append(snake.points)

  for i in range(0, snake_len):
    print_overwrite(f"Creating Lines volume {pad_max(i + 1, snake_len)}")
    node = snake.list[i]
    point = node.point
    size = node.size
    perpendicular = node.final_vec.perpendicular_copy()
    line0 = Line(point, point.add_copy(perpendicular.multiply_copy(size)))
    line1 = Line(point, point.add_copy(perpendicular.multiply_copy(-size)))
    node.lines.append(line0)
    node.lines.append(line1)

  print_overwrite("Creating ribs...")
  for i in range(0, snake_len):
    print_overwrite(f"Creating rib {pad_max(i + 1, snake_len)}")
    node = snake.list[i]
    for ribline in node.lines:
      ribs_subdivide = subdivide_point_path(ribline.points(), rib_sub_count)

      shuffle_amount = raw_shuffle_amount * ribline.length()
      if not options.get('do_rib_shuffle', True):
        shuffle_amount = 0
      shuffle = node.final_vec.multiply_copy(shuffle_amount)

      for j in forward_indices:
        ribs_subdivide[j].add(shuffle)
      for j in backward_indices:
        ribs_subdivide[j].subtract(shuffle)

      # centers = generate_centerpoints(ribs_subdivide)
      # final_rib = generate_final_points(ribs_subdivide, centers, 1)
      final_points.append(ribs_subdivide)

  print_finish_overwite()

  return final_points
