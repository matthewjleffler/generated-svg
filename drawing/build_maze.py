from lib import *


###
### Space filling curve algorithm based on:
### https://observablehq.com/@esperanc/random-space-filling-curves
###

class MazeSize:
  def __init__(self, cell_size: float, rect: Rect, cutout_range: float = 0):
    self.row = floor(rect.h / cell_size)
    self.row2 = self.row * 2
    self.col = floor(rect.w / cell_size)
    self.col2 = self.col * 2
    self.total = self.row * self.col
    self.total2 = self.row2 * self.col2

    node_w = rect.w / self.col2
    node_h = rect.h / self.row2
    node = min(node_w, node_h)

    self.node_w = self.node_h = node
    self.node_scale = Point(self.node_w, self.node_h)
    self.half_w = self.node_w / 2
    self.half_h = self.node_h / 2

    self.origin = Point(rect.x + self.half_w, rect.y + self.half_h)

    self.range_stamp = floor(min(self.col * cutout_range, self.row * cutout_range))


class MazeOptions:
  close_path: bool
  do_inset: bool


# A 'type definition'
class PushOptions:
  debug_draw_boundary: bool
  do_push: bool
  random_push: bool
  push_pad_range_max: float
  push_pad_range_offset: float
  push_num: RangeInt
  push_line_cell_size: RangeFloat
  push_line_step_size: float
  push_range: RangeFloat
  push_strength: RangeFloat


class _Pusher:
  def __init__(self, origin: Point, params: PushOptions):
    self.origin = origin
    self.range = params.push_range.rand()
    self.strength = params.push_strength.rand()


class _Connect:
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


def _spanning_tree(row: int, col: int, total: int, range_stamp: int, do_inset: bool) -> List[tuple[int, int]]:
  grid = [False] * total
  totalRange = RangeInt(0, total - 1)

  if range_stamp > 0:
    center = Point(col / 2, row / 2)
    for o_x in range(-range_stamp, range_stamp+1):
      for o_y in range(-range_stamp, range_stamp+1):
        if do_inset and o_x == 0 and o_y < range_stamp - 2:
          continue
        loc = center.add_floats_copy(o_x, o_y)
        delta = loc.subtract_copy(center)
        if delta.length() > range_stamp:
          continue
        (x_int, y_int) = loc.to_int()
        i = _x_y_to_index(x_int, y_int, col)
        grid[i] = True

  edges: List[tuple[int, int]] = []

  # Pick start until we get a valid one TODOML more efficient?
  while True:
    start = totalRange.rand()
    if grid[start] == False:
      break

  next_visit: List[tuple[int, List[int]]] = [(-1, [start])]
  while (len(next_visit) > 0):
    (last, next) = next_visit[0]
    if len(next) <= 0:
      next_visit.pop(0)
      continue
    index = next.pop(0)
    new_visits = _visit(index, last, row, col, grid, edges)
    if new_visits:
      next_visit.insert(0, (index, new_visits))
  return edges


def _hamiltonian_from_spanning_tree(col: int, col2: int, total2: int, connect: List[_Connect]) -> List[int]:
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


def make_maze_line(size: MazeSize, options: MazeOptions) -> List[Point]:
  reload_libs(globals())

  edges = _spanning_tree(size.row, size.col, size.total, size.range_stamp, options.do_inset)

  connect: List[_Connect] = []
  for i in range(0, size.total):
    connect.append(_Connect())

  for (i0, i1) in edges:
    f0 = i0
    f1 = i1
    if i0 > i1:
      f0 = i1
      f1 = i0
    y0 = _index_to_x_y(f0, size.col)[1]
    y1 = _index_to_x_y(f1, size.col)[1]
    if y0 == y1:
      connect[f0].right = connect[f1].left = True
    else:
      connect[f0].down = connect[f1].up = True

  # Debug drawing the initial maze lines
  # for (i0, i1) in edges:
  #   (x0, y0) = _index_to_x_y(i0, size.col)
  #   (x1, y1) = _index_to_x_y(i1, size.col)
  #   debug_line = Line(Point(x0, y0), Point(x1, y1))
  #   draw_point_path(debug_line.multiply(size.node_scale).add(size.origin).points())
  # return []

  path = _hamiltonian_from_spanning_tree(size.col, size.col2, size.total2, connect)

  # Prune bad edges, if we have a subset of the whole image
  for i in range(0, len(path)):
    point = path[i]
    if point == 0 and i > 0:
      del path[i: len(path)]
      break

  # Offset the path randomly
  offsetPath: List[int] = []
  pathlen = len(path)
  offset = RangeInt(0, pathlen - 1).rand()
  for i in range(0, pathlen):
    index = (offset + i) % pathlen
    offsetPath.append(path[index])
  if options.close_path:
    offsetPath.append(path[offset])

  # Scale and shuffle the points
  line: List[Point] = []
  offsetPathLen = len(offsetPath)
  for i in range(0, offsetPathLen):
    index = offsetPath[i]
    (x, y) = _index_to_x_y(index, size.col2)
    line.append(Point(x, y).multiply_point(size.node_scale).add(size.origin))

  return line

def push_line(line: List[Point], rect: Rect, params: PushOptions, group: Group) -> Rect:
  return push_lines([line], rect, params, group)

def push_lines(lines: List[List[Point]], rect: Rect, params: PushOptions, group: Group) -> Rect:
  reload_libs(globals())

  # Do push randomization independent of draw
  pushers: List[_Pusher] = []
  pad_x = rect.w * params.push_pad_range_max
  pad_y = rect.h * params.push_pad_range_max
  pad_offset_x = rect.w * params.push_pad_range_offset
  pad_offset_y = rect.h * params.push_pad_range_offset
  push_pad_x = RangeFloat(-pad_x, pad_x)
  push_pad_y = RangeFloat(-pad_y, pad_y)
  push_pad_offset_x = RangeFloat(-pad_offset_x, pad_offset_x)
  push_pad_offset_y = RangeFloat(-pad_offset_y, pad_offset_y)
  push_rect = rect.shrink_xy_copy(push_pad_x.rand(), push_pad_y.rand())
  push_rect.x += push_pad_offset_x.rand()
  push_rect.y += push_pad_offset_y.rand()
  if params.random_push:
    num_pushers = params.push_num.rand()
    for _ in range(0, num_pushers):
      origin = Point(RangeFloat(push_rect.x, push_rect.right()).rand(), RangeFloat(push_rect.y, push_rect.bottom()).rand())
      pushers.append(_Pusher(origin, params))
  else:
    push_cell = params.push_line_cell_size.rand()
    push_size = MazeSize(push_cell, push_rect)
    push_options = MazeOptions()
    push_options.close_path = True
    push_options.do_inset = False
    push_line = make_maze_line(push_size, push_options)
    push_center = generate_centerpoints(push_line)
    push_divisions = generate_final_points(push_line, push_center, params.push_line_step_size)

    # Draw debug
    # new_group = open_group(GroupSettings(stroke=GroupColor.red), group)
    # draw_point_circles(push_divisions, new_group)
    # close_group()

    for point in push_divisions:
      pushers.append(_Pusher(point, params))

  # Draw push
  if params.do_push:
    push_index = 0
    print_overwrite('Pushing...')
    for push in pushers:
      push_index += 1
      print_overwrite(f"Running push {pad_max(push_index, len(pushers))} ...")
      for line in lines:
        for point in line:
          delta = point.subtract_copy(push.origin)
          delta_len = delta.length()
          if delta_len > push.range:
            continue
          t = 1 - (delta_len / push.range)
          push_amount = ease_in_out_quad(t, 0, push.strength, 1)
          point.add(delta.normalize().multiply(push_amount))
    print_finish_overwite()

  return push_rect
