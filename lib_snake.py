from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from typing import List

###
### Snake Bones
###

###
### Space filling curve algorithm based on:
### https://observablehq.com/@esperanc/random-space-filling-curves
###

class SnakeParams:
  def __init__(self) -> None:
    self.draw: bool = True
    self.pad: int = 50
    self.draw_head: bool = True
    self.row: RangeInt = RangeInt(3, 10)
    self.diff: RangeInt = RangeInt(0, 5)
    self.shuffle: RangeFloat = RangeFloat(.001, .5)
    self.do_shuffle: bool = True
    self.step_dist: int = 3 # 3
    self.min_dist: int = 1
    self.size_start: int = 5
    self.size_increase: float = .25
    self.dot_threshhold: float = 0
    self.index_range: int = 1000 / self.step_dist
    self.falloff: float = .02
    self.min_falloff: int = 0
    self.spine_count: RangeInt = RangeInt(5, 5)
    self.do_spine_shuffle: bool = True
    self.spine_shuffle: float = .1
    self.smoothing_steps: int = 4 # 10
    self.smoothing_range: int = floor(30 / self.step_dist)
    self.draw_ribs: bool = True
    self.draw_spine: bool = True
    self.draw_reverse: bool = False


class SnakeNode:
  def __init__(self, point: Point, index: int, params: SnakeParams) -> None:
    self.point = point
    self.index = index
    self.size = params.size_start
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

  def add(self, point: Point, params: SnakeParams) -> SnakeNode:
    node = SnakeNode(point, len(self.list), params)
    self.list.append(node)
    return node


class Connect:
  def __init__(self) -> None:
    self.right = False
    self.left = False
    self.up = False
    self.down = False


def _x_y_to_index(x: int, y: int, w: int) -> int:
  return y * w + x

def _index_to_x_y(index: int, w: int) -> tuple[int, int]:
  return (int(index % w), int(index / w))


def _check_other_points(
    snake: Snake,
    node: SnakeNode,
    new_size: int,
    params: SnakeParams
  ) -> bool:
  for node_other in snake.list:
    if node == node_other:
      # Same node
      continue

    delta = node_other.point.subtract_copy(node.point)
    if delta.length() > new_size + node_other.size:
      # Not too close
      continue

    dot = node.vec().dot(node_other.vec())
    if dot >= params.dot_threshhold and abs(node.index - node_other.index) < params.index_range:
      # Allowed, close enough and part of the same line
      continue

    # Blocked
    node.done = True
    return False

  # Not blocked
  node.size = new_size
  return True


def visit(index: int, row: int, col: int, grid: List[bool], edges: List[tuple[int, int]]) -> None:
  grid[index] = True
  (x, y) = _index_to_x_y(index, col)
  neighbors: List[int] = []
  if x > 0:
    neighbors.append(_x_y_to_index(x - 1, y, col))
  if y > 0:
    neighbors.append(_x_y_to_index(x, y - 1, col))
  if x < col - 1:
    neighbors.append(_x_y_to_index(x + 1, y, col))
  if y < row - 1:
    neighbors.append(_x_y_to_index(x, y + 1, col))
  order = []
  while len(neighbors) > 0:
    n = RangeInt(0, len(neighbors) - 1).rand()
    neighbor = neighbors.pop(n)
    order.append(neighbor)
    if grid[neighbor]:
      continue
    edges.append((index, neighbor))
    visit(neighbor, row, col, grid, edges)


def spanning_tree(row: int, col: int, total: int) -> List[tuple[int, int]]:
  grid = [False] * total
  edges: List[tuple[int, int]] = []
  start = RangeInt(0, total - 1).rand()
  visit(start, row, col, grid, edges)
  return edges

def _index2(i: int, dcol: int, drow: int, w: int, w2: int) -> int:
  [x, y] = _index_to_x_y(i, w)
  return (y * 2 + drow) * w2 + x * 2 + dcol

def hamiltonian_from_spanning_tree(col: int, col2: int, total2: int, connect: List[Connect]) -> List[int]:
  edges2: List[tuple[int, int]] = []
  for i in range(0, len(connect)):
    cell = connect[i]
    if cell.right:
      edges2.append((_index2(i, 1, 0, col, col2), _index2(i, 2, 0, col, col2)))
      edges2.append((_index2(i, 1, 1, col, col2), _index2(i, 2, 1, col, col2)))
    else:
      edges2.append((_index2(i, 1, 0, col, col2), _index2(i, 1, 1, col, col2)))
    if not cell.left:
      edges2.append((_index2(i, 0, 0, col, col2), _index2(i, 0, 1, col, col2)))
    if cell.down:
      edges2.append((_index2(i, 0, 1, col, col2), _index2(i, 0, 2, col, col2)))
      edges2.append((_index2(i, 1, 1, col, col2), _index2(i, 1, 2, col, col2)))
    else:
      edges2.append((_index2(i, 0, 1, col, col2), _index2(i, 1, 1, col, col2)))
    if not cell.up:
      edges2.append((_index2(i, 0, 0, col, col2), _index2(i, 1, 0, col, col2)))
  link: List[List[int]] = []
  visited: List[int] = []
  for i in range(total2):
    link.append([])
    visited.append(False)
  for (i, j) in edges2:
    link[i].append(j)
    link[j].append(i)
  j = 0
  path: List[int] = []
  for _ in range(0, len(edges2)):
    path.append(j)
    visited[j] = True
    if visited[link[j][0]]:
      j = link[j][1]
    else:
      j = link[j][0]
  return path

def draw_snake(params: SnakeParams, group: Group = None):
  # draw_border(group)

  max_pad = svg_safe().copy()
  pad = svg_safe().shrink_copy(params.pad)

  # Draw safety border and page border
  # draw_rect_rect(pad, group)
  # draw_rect_rect(svg_full())

  row = params.row.rand()
  row2 = row * 2
  diff = params.diff.rand()
  col = row + diff
  col2 = col * 2
  total = row * col
  total2 = row2 * col2

  node_w = pad.w / (col2)
  node_h = pad.h / (row2)
  half_w = node_w / 2
  half_h = node_h / 2
  min_size = min(half_w, half_h)
  size_increase = params.size_increase * min_size

  edges = spanning_tree(row, col, total)

  connect: List[Connect] = []
  for i in range(0, total):
    connect.append(Connect())

  for (i0, i1) in edges:
    f0 = i0
    f1 = i1
    if i0 > i1:
      f0 = i1
      f1 = i0
    y0 = _index_to_x_y(f0, col)[1]
    y1 = _index_to_x_y(f1, col)[1]
    if y0 == y1:
      connect[f0].right = connect[f1].left = True
    else:
      connect[f0].down = connect[f1].up = True

  # Debug drawing the initial maze lines
  # for (i0, i1) in edges:
  #   (x0, y0) = _index_to_x_y(i0, col)
  #   (x1, y1) = _index_to_x_y(i1, col)
  #   line = Line(Point(x0, y0), Point(x1, y1))
  #   draw_point_path(line.multiply(Point(node_w, node_h)).add(Point(pad.x, pad.y)).points(), group)
  # return

  path = hamiltonian_from_spanning_tree(col, col2, total2, connect)

  # Offset the path randomly
  offsetPath: List[int] = []
  pathlen = len(path)
  offset = RangeInt(0, pathlen - 1).rand()
  for i in range(0, pathlen):
    index = (offset + i) % pathlen
    offsetPath.append(path[index])

  # Scale and shuffle the points
  line: List[Point] = []
  for i in offsetPath:
    (x, y) = _index_to_x_y(i, col2)
    point = Point(x, y)
    point.x *= node_w
    point.y *= node_h
    point.x += pad.x + half_w
    point.y += pad.y + half_h
    if params.do_shuffle:
      point.x += params.shuffle.rand() * half_w
      point.y += params.shuffle.rand() * half_h
    line.append(point)

  # Debug draw the line
  # draw_point_path(line)
  # return

  # Generate flowing lines
  ribs_subdivide_centers = generate_centerpoints(line)
  points = generate_final_points(line, ribs_subdivide_centers, params.step_dist)
  snake = Snake(points, ribs_subdivide_centers)
  for i in range(0, len(points)):
    node = snake.add(points[i], params)
    if i > 0:
      snake.list[i-1].set_next(node)

  print("Nodes:", len(points))

  # Iterate through each point, increase size until it's out of bounds
  # or no further changes can be made
  # TODOML wildly inefficient
  iterations = 0
  madeChange = True
  while (madeChange):
    madeChange = False
    iterations += 1
    if iterations % 5 == 0:
      print("Running iteration", iterations, "...")

    for node in snake.list:
      if node.done:
        continue

      # Try to increase size
      point = node.point
      new_size = node.size + size_increase

      top = point.y - new_size
      bottom = point.y + new_size
      left = point.x - new_size
      right = point.x + new_size

      # Check against border
      if top < max_pad.y:
        node.done = True
        continue
      elif bottom > max_pad.bottom():
        node.done = True
        continue
      elif left < max_pad.x:
        node.done = True
        continue
      elif right > max_pad.right():
        node.done = True
        continue

      madeChange = _check_other_points(snake, node, new_size, params) or madeChange

  print("Ran", iterations, "iterations")

  # Shrink ends
  length = len(snake.list)
  falloff = floor(max(length * params.falloff, params.min_falloff))
  for node in snake.list:
    percent_bot = node.index / falloff
    percent_end = (length - 1 - node.index) / falloff
    percent = min(percent_bot, percent_end)
    percent = min(percent, 1)
    node.size = ease_in_out_quad(percent, 0, node.size, 1)

  # Average Sizes
  for iterations in range(0, params.smoothing_steps):
    snake_len = len(snake.list)
    for i in range(0, snake_len):
      from_end = min(i, snake_len - 1 - i)
      steps = min(from_end, params.smoothing_range)
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
      current.final_vec = avg_vec.divide(total_steps)

  # Create lines
  rib_index = 0
  for node in snake.list:
    rib_index += 1
    point = node.point
    size = node.size
    perpendicular = node.final_vec.perpendicular_copy()
    line0 = Line(point, point.add_copy(perpendicular.multiply_copy(size)))
    line1 = Line(point, point.add_copy(perpendicular.multiply_copy(-size)))
    # Alternate direction so pen can travel smoothly
    if rib_index % 2 == 0 or not params.draw_reverse:
      node.lines.append(line0)
      node.lines.append(line1)
    else:
      node.lines.append(line1)
      node.lines.append(line0)

  forward_indices = [1, 5]
  backward_indices = [2, 3]

  # Draw Result
  if params.draw_spine:
    if params.draw_head:
      head_point = snake.points[0]
      draw_circ(head_point.x, head_point.y, 20, group)
    draw_point_path(snake.points, group)

  rib_index = 0
  for node in snake.list:
    for ribline in node.lines:
      ribs_subdivide = subdivide_point_path(ribline.points(), params.spine_count)

      shuffle_amount = params.spine_shuffle * ribline.length()
      if not params.do_spine_shuffle:
        shuffle_amount = 0
      shuffle = node.final_vec.multiply_copy(shuffle_amount)

      for i in forward_indices:
        ribs_subdivide[i].add(shuffle)
      for i in backward_indices:
        ribs_subdivide[i].subtract(shuffle)

      # Reverse them so the pen can travel smoothly
      if params.draw_reverse and rib_index % 2 == 0:
        ribs_subdivide.reverse()
      rib_index += 1

      ribs_subdivide_centers = generate_centerpoints(ribs_subdivide)
      if params.draw_ribs:
        draw_curved_path(ribs_subdivide, ribs_subdivide_centers, group)
