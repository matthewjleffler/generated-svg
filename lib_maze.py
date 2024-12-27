from lib import *
from lib_path import *
from typing import List

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


def _index2(i: int, dcol: int, drow: int, w: int, w2: int) -> int:
  [x, y] = _index_to_x_y(i, w)
  return (y * 2 + drow) * w2 + x * 2 + dcol


def _visit(
    index: int,
    last: int,
    row: int,
    col: int,
    grid: List[bool],
    edges: List[tuple[int, int]]
  ) -> List[int]:
  if grid[index]:
    return None

  if last >= 0:
    edges.append((last, index))

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
    if grid[neighbor]:
      continue
    order.append(neighbor)

  return order


def _spanning_tree(row: int, col: int, total: int) -> List[tuple[int, int]]:
  grid = [False] * total
  edges: List[tuple[int, int]] = []
  start = RangeInt(0, total - 1).rand()
  next_visit: List[tuple[int, List[int]]] = [(-1, [start])]
  while (len(next_visit) > 0):
    (last, next) = next_visit[0]
    if len(next) <= 0:
      next_visit.pop(0)
      continue
    index = next.pop(0)
    new_visits = _visit(index, last, row, col, grid, edges, )
    if new_visits:
      next_visit.insert(0, (index, new_visits))
  return edges


def _hamiltonian_from_spanning_tree(col: int, col2: int, total2: int, connect: List[Connect]) -> List[int]:
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


def make_maze_line(
    row: int,
    col: int,
    node_w: float,
    node_h: float,
    origin_x: float,
    origin_y: float,
    close_path: bool
  ) -> List[Point]:
  total = row * col
  row2 = row * 2
  col2 = col * 2
  total2 = row2 * col2

  edges = _spanning_tree(row, col, total)

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
  #   draw_point_path(line.multiply(Point(node_w, node_h)).add(Point(x, y)).points())
  # return []

  path = _hamiltonian_from_spanning_tree(col, col2, total2, connect)

  # Offset the path randomly
  offsetPath: List[int] = []
  pathlen = len(path)
  offset = RangeInt(0, pathlen - 1).rand()
  for i in range(0, pathlen):
    index = (offset + i) % pathlen
    offsetPath.append(path[index])
  if close_path:
    offsetPath.append(path[offset])

  # Scale and shuffle the points
  line: List[Point] = []
  offsetPathLen = len(offsetPath)
  for i in range(0, offsetPathLen):
    index = offsetPath[i]
    (x, y) = _index_to_x_y(index, col2)
    line.append(Point(x, y).multiply_floats(node_w, node_h).add_floats(origin_x, origin_y))

  return line