from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from typing import List

###
### Snake Bones
###

class SnakeParams:
  def __init__(self) -> None:
    self.draw: bool = True
    self.draw_head: bool = True
    self.row: RangeInt = RangeInt(3, 10)
    self.diff: RangeInt = RangeInt(0, 10)
    self.shuffle: RangeFloat = RangeFloat(.001, .5)
    self.do_shuffle: bool = True
    self.min_len: int = 2
    self.step_dist: int = 10
    self.size_start: int = 5
    self.size_increase: int = 5
    self.dot_threshhold: float = -.5
    self.delta_threshold: float = 20
    self.index_range: int = 40
    self.falloff: float = .1
    self.min_falloff: int = 3
    self.final_step_dist: int = 5
    self.spine_count: RangeInt = RangeInt(5, 5)
    self.do_spine_shuffle: bool = True
    self.spine_shuffle: float = .1
    self.smoothing_steps: int = 10
    self.smoothing_range: int = 3
    self.draw_ribs: bool = True
    self.draw_spine: bool = True


class SnakeNode:
  def __init__(self, point: Point, index: int, params: SnakeParams) -> None:
    self.point = point
    self.index = index
    self.size = params.size_start
    self.next: SnakeNode = None
    self.end_point: Point = None
    self.final_vec: Point = Point(0, 0)
    self.lines: List[Line] = []

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

  def add(self, point: Point, params: SnakeParams) -> SnakeNode:
    node = SnakeNode(point, len(self.list), params)
    self.list.append(node)
    return node


class SnakeList:
  def __init__(self) -> None:
    self.list: List[Snake] = []

  def add(self, points: List[Point], centers: List[Point]) -> Snake:
    snake = Snake(points, centers)
    self.list.append(snake)
    return snake


def _x_y_to_index(x, y, w):
  return y * w + x

def _index_to_x_y(index, w):
  return (int(index % w), int(index / w))

def _pick_remaining(available: List[bool], w: int) -> Point:
  possible: List[Point] = []
  for i in range(0, len(available)):
    if available[i] == False:
      continue
    (x, y) = _index_to_x_y(i, w)
    possible.append(Point(x, y))
  return possible[rand_int(0, len(possible) - 1)]

def _find_near(x, y, available, w, h):
  result: List[Point] = []
  if y > 0 and available[_x_y_to_index(x, y - 1, w)]:
    result.append(Point(x, y - 1))
  if x > 0 and available[_x_y_to_index(x - 1, y, w)]:
    result.append(Point(x - 1, y))
  if y < h - 1 and available[_x_y_to_index(x, y + 1, w)]:
    result.append(Point(x, y + 1))
  if x < w - 1 and available[_x_y_to_index(x + 1, y, w)]:
    result.append(Point(x + 1, y))
  return result


def find_intersections(line: Line, index: int, other_snake: Snake) -> Point:
  length = line.length()
  shortest = length
  intersection = None
  for other_node in other_snake.list:
    other_line = other_node.lines[index]
    if other_line == line:
      # Don't compare same line
      continue
    new_intersection = line_intersection(line, other_line)
    if new_intersection is None:
      continue
    delta = Line(other_line.p0, new_intersection).length()
    if delta > other_line.length():
      continue
    int_line = Line(line.p0, new_intersection)
    if int_line.dot(line) < 1:
      continue
    delta = int_line.length()
    if delta > length:
      continue
    if delta >= shortest:
      continue
    intersection = new_intersection
    shortest = delta

  return intersection


def clamp_sizes(final: SnakeList) -> None:
  # Check all lines for intersections with each other
  for snake in final.list:
    for node in snake.list:
      for i in range(0, 2):
        line = node.lines[i]
        intersection = find_intersections(line, i, snake)
        if intersection is not None:
          line.p1 = intersection


def check_other_points(
    final: SnakeList,
    snake: Snake,
    node: SnakeNode,
    new_size: int,
    params: SnakeParams
  ) -> bool:
  for snake_other in final.list:
    for node_other in snake_other.list:
      if snake == snake_other and node == node_other:
        # Same node
        continue

      delta = node_other.point.subtract_copy(node.point)
      if delta.length() > new_size + node_other.size:
        # Not too close
        continue

      dot = node.vec().dot(node_other.vec())
      if snake == snake_other and dot >= params.dot_threshhold and abs(node.index - node_other.index) < params.index_range:
        # Allowed, close enough and part of the same line
        continue

      # Blocked
      delta.normalize().multiply(node.size)
      node.end_point = node.point.add_copy(delta)
      return False

  # Not blocked
  node.size = new_size
  return True


def draw_snake(params: SnakeParams, group: Group = None):
  # draw_border(group)

  pad = svg_safe().copy()
  row = params.row.rand()
  diff = params.diff.rand()
  col = row + diff
  total = row * col
  remaining = total

  node_w = pad.w / (row)
  node_h = pad.h / (col)
  half_w = node_w / 2
  half_h = node_h / 2
  min_w = min(half_w, half_h)

  # Create nodes
  available: List[bool] = [True] * total
  lines: List[List[Point]] = []
  while remaining > 0:
    next = _pick_remaining(available, row) # pick randomly from remaining
    available[_x_y_to_index(next.x, next.y, row)] = False
    remaining -= 1
    line: List[Point] = [next]
    lines.append(line)
    while True:
      near = _find_near(next.x, next.y, available, row, col) # Check available nearby and add to this list
      if len(near) < 1:
        break
      next = near[rand_int(0, len(near) - 1)] # Pick random nearby
      available[_x_y_to_index(next.x, next.y, row)] = False
      remaining -= 1
      line.append(next)

  if len(lines) < 1:
    print("No lines generated")
    return

  # Scale from checkerboard into image space
  scaled_lines: List[List[Point]] = []
  for line in lines:
    # Not long enough
    if len(line) < params.min_len:
      continue

    # Add the padding and scale the point
    for p in line:
      s_x = params.shuffle.rand() * half_w
      s_y = params.shuffle.rand() * half_h
      if not params.do_shuffle:
        s_x = 0
        s_y = 0

      p.x = s_x + pad.x + half_w + p.x * node_w
      p.y = s_y + pad.y + half_h + p.y * node_h

    # Record the updated line
    scaled_lines.append(line)

  # Generate flowing lines
  final = SnakeList()
  for line in scaled_lines:
    ribs_subdivide_centers = generate_centerpoints(line)
    points = generate_final_points(line, ribs_subdivide_centers, params.step_dist, 3)
    snake = final.add(line, ribs_subdivide_centers)
    for i in range(0, len(points)):
      node = snake.add(points[i], params)
      if i > 0:
        snake.list[i-1].set_next(node)

  # Iterate through each point, increase size until it's out of bounds
  # or no further changes can be made
  # TODOML wildly inefficient
  iterations = 0
  madeChange = True
  while (madeChange):
    madeChange = False
    iterations += 1

    for snake in final.list:
      for node in snake.list:
        # Try to increase size
        point = node.point
        new_size = node.size + params.size_increase

        top = point.y - new_size
        bottom = point.y + new_size
        left = point.x - new_size
        right = point.x + new_size

        # Check against border
        if top < pad.y:
          node.end_point = Point(point.x, pad.y)
          continue
        elif bottom > pad.bottom():
          node.end_point = Point(point.x, pad.bottom())
          continue
        elif left < pad.x:
          node.end_point = Point(pad.x, point.y)
          continue
        elif right > pad.right():
          node.end_point = Point(pad.right(), point.y)
          continue

        madeChange = check_other_points(final, snake, node, new_size, params) or madeChange

  # Average Sizes
  for snake in final.list:
    for iterations in range(0, params.smoothing_steps):
      for i in range(0, len(snake.list)):
        steps = 1
        current = snake.list[i]
        avg_size = current.size
        avg_vec = current.final_vec.copy()
        for j in range(i-params.smoothing_range, i + params.smoothing_range + 1):
          if j == i or j < 0 or j >= len(snake.list):
            continue
          steps += 1
          node = snake.list[j]
          avg_size += node.size
          avg_vec.add(node.final_vec)
        current.size = avg_size / steps
        current.final_vec = avg_vec.divide(steps)

  # Shrink ends
  for snake in final.list:
    length = len(snake.list)
    falloff = max(length * params.falloff, params.min_falloff)
    for node in snake.list:
      percent_bot = node.index / falloff
      percent_end = (length - 1 - node.index) / falloff
      percent = min(percent_bot, percent_end)
      percent = min(percent, 1)
      node.size = ease_in_out_quad(percent, params.size_start, node.size - params.size_start, 1)

  # Create lines
  for snake in final.list:
    for node in snake.list:
      point = node.point
      size = node.size
      perpendicular = node.final_vec.perpendicular_copy()
      node.lines.append(Line(point, point.add_copy(perpendicular.multiply_copy(size))))
      node.lines.append(Line(point, point.add_copy(perpendicular.multiply_copy(-size))))

  # clamp_sizes(final)

  forward_indices = [1, 5]
  backward_indices = [2, 3]
  count = params.spine_count.rand() + 1

  # Draw Result
  for snake in final.list:
    if params.draw_spine:
      draw_curved_path(snake.points, snake.centers, group)
      if params.draw_head:
        head_point = snake.points[0]
        draw_circ(head_point.x, head_point.y, 20, group)

    for node in snake.list:
      for ribline in node.lines:
        ribs_subdivide = subdivide_point_path(ribline.points(), params.spine_count)
        if len(ribs_subdivide) < count:
          break

        # draw_point_path(ribs_subdivide, group)

        shuffle_amount = params.spine_shuffle * ribline.length()
        if not params.do_spine_shuffle:
          shuffle_amount = 0
        shuffle = node.final_vec.multiply_copy(shuffle_amount)

        for i in forward_indices:
          ribs_subdivide[i].add(shuffle)
        for i in backward_indices:
          ribs_subdivide[i].subtract(shuffle)

        ribs_subdivide_centers = generate_centerpoints(ribs_subdivide)
        if params.draw_ribs:
          draw_curved_path(ribs_subdivide, ribs_subdivide_centers, group)
