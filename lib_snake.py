from lib_math import *
from lib_path import *
from typing import List


class SnakeNode:
  def __init__(self, point: Point, index: int, width: float) -> None:
    self.point = point
    self.index = index
    self.size = width
    self.next: SnakeNode = None
    self.final_vec: Point = Point(0, 0)
    self.lines: List[Line] = []
    self.done = False

  def set_next(self, next: 'SnakeNode') -> None:
    self.next = next
    self.final_vec = self.vec()

  def vec(self) -> Point:
    if self.next is None:
      return Point(0, 0)
    return self.next.point.subtract_copy(self.point).normalize()


class Snake:
  def __init__(self, points: List[Point], centers: List[Point]) -> None:
    self.list: List[SnakeNode] = []
    self.points = points
    self.centers = centers

  def add(self, point: Point, width: float) -> SnakeNode:
    node = SnakeNode(point, len(self.list), width)
    self.list.append(node)
    return node


class SnakeDrawParams:
  def __init__(
      self,
      draw_spine: bool,
      draw_head: bool,
      draw_ribs: bool,
      step_dist: int,
      num_divisions: int,
      division_range: RangeFloat,
      max_size: float,
      end_falloff: float,
      do_average: bool,
      smoothing_range: float,
      smoothing_steps: int,
      do_inflate_corners: bool,
      inflate_factor: float,
      do_final_average: bool,
      final_average_weight: int,
      do_rib_shuffle: bool,
      rib_shuffle_amount: float,
    ):
    self.draw_spine = draw_spine
    self.draw_head = draw_head
    self.draw_ribs = draw_ribs
    self.step_dist = step_dist
    self.num_divisions = num_divisions
    self.end_falloff = end_falloff
    self.do_average = do_average
    self.smoothing_range = smoothing_range
    self.smoothing_steps = smoothing_steps
    self.do_inflate_corners = do_inflate_corners
    self.inflate_factor = inflate_factor
    self.do_final_average = do_final_average
    self.final_average_weight = final_average_weight
    self.do_rib_shuffle = do_rib_shuffle
    self.rib_shuffle_amount = rib_shuffle_amount

    # Set up divisions
    self.division_size: List[float] = []
    for _ in range(0, num_divisions + 1):
      self.division_size.append(max_size * division_range.rand())


def draw_snake_from_points(line: List[Point], params: SnakeDrawParams, rect: Rect, group: Group = None):
  # Generate flowing lines
  ribs_subdivide_centers = generate_centerpoints(line)
  points = generate_final_points(line, ribs_subdivide_centers, params.step_dist)
  snake = Snake(points, ribs_subdivide_centers)
  len_points = len(points)
  print("Nodes:", len_points)
  division_points = len_points / params.num_divisions
  for i in range(0, len_points):
    division = params.division_size[floor(i / division_points)]
    node = snake.add(points[i], division)
    if i > 0:
      snake.list[i-1].set_next(node)

  # Shrink ends
  length = len(snake.list)
  falloff = floor(length * params.end_falloff)
  for node in snake.list:
    percent_bot = node.index / falloff
    percent_end = (length - 1 - node.index) / falloff
    percent = min(percent_bot, percent_end)
    percent = min(percent, 1)
    node.size = ease_in_out_quad(percent, 0, node.size, 1)

  # Average Sizes
  smoothing_range: int = floor(params.smoothing_range / params.step_dist)
  snake_len = len(snake.list)
  if params.do_average:
    for _ in range(0, params.smoothing_steps):
      for i in range(0, snake_len):
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
    for node in snake.list:
      dot = 1 - abs(node.vec().dot(node.final_vec))
      node.size *= (1 + (dot) * params.inflate_factor)

  # One more average, sizes only
  if params.do_average:
    for _ in range(0, params.smoothing_steps):
      for i in range(0, snake_len):
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
    for node in snake.list:
      avg_vec = node.vec()
      for _ in range(0, params.final_average_weight):
        avg_vec.add(node.final_vec)
      node.final_vec = avg_vec.divide(params.final_average_weight + 1)

  # Create lines
  expand = ExpandingVolume()
  for node in snake.list:
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

  # Draw Result
  if params.draw_spine:
    if params.draw_head:
      head_point = snake.points[0]
      draw_circ(head_point.x, head_point.y, 20, scaled)
    draw_point_path(snake.points, scaled)

  if params.draw_ribs:
    for node in snake.list:
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
