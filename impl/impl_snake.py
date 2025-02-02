from lib import *
import drawing.build_triangle as build_triangle
import drawing.build_maze as build_maze
import drawing.build_snake as build_snake
import drawing.build_push as build_push


###
### Snake Bones
###

###
### Space filling curve algorithm based on:
### https://observablehq.com/@esperanc/random-space-filling-curves
###

class _SnakeType(ReloadEnum):
  maze = 0
  triangle = 1

class SnakeParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.debug_draw_boundary: bool = True
    self.debug_draw_points: bool = False
    self.cell_size = 280
    self.line_type: _SnakeType = _SnakeType.maze
    self.spine_factor: float = .15
    self.do_cap: bool = False
    self.cap_percent: RangeFloat = RangeFloat(.5, .99)

    # SnakeOptions
    self.draw_spine: bool = False
    self.draw_head: bool = False
    self.draw_ribs: bool = True
    # 3 for sharpie pens, 4 (3.5?) for 0.5 isograph
    self.step_dist: float = 1
    self.do_inflate: bool = False
    self.inflate_factor: float = 1
    self.end_falloff: float = .15
    self.do_average: bool = True
    self.smoothing_range: int = 120
    self.smoothing_steps: int = 3
    self.do_inflate_corners: bool = True
    self.inflate_corner_factor: float = 2
    self.do_final_average: bool = False
    self.final_average_weight: int = 2
    self.do_rib_shuffle: bool = True
    self.raw_shuffle_amount: RangeFloat = RangeFloat(.05, .5)
    self.break_count: int = 200
    self.original_ribs: bool = False
    self.rib_range: RangeInt = RangeInt(3, 10)

    # MazeOptions
    self.close_path: bool = False
    self.do_inset: bool = False

    # PushOptions
    self.do_push: bool = True
    self.push_settings = [
      create({ 'strength': 10, 'strength_octave': 70, 'rotation_octave': 5 }),
      create({ 'strength': 300, 'strength_octave': 2.5 })
    ]

    # TriangleOptions
    self.triangle_step_size = 100

    super().__init__(defaults)


def draw_snake(params: SnakeParams, group: Group, seed: int):
  reload_libs(globals())

  pad = svg_safe().copy()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  if params.line_type == _SnakeType.maze:
    maze_size = build_maze.MazeSize(params.cell_size, pad)

    # Make maze
    line: List[Point] = build_maze.make_maze_line(maze_size, params)
    if len(line) < 1:
      print('0 length maze')
      return
    inflate_step = max(int(min(maze_size.half_w / 2, maze_size.half_h / 2)), 5)
  elif params.line_type == _SnakeType.triangle:
    triangle_result = build_triangle.create_triangle_lines(pad, params)
    line = triangle_result.triangle_points
    inflate_step = max(int(params.triangle_step_size / 4), 5)

  # Re-init randomness after maze
  random.seed(seed)

  # Cap line
  cap_percent = params.cap_percent.rand()
  cap_index = floor(len(line) * cap_percent)
  if params.do_cap:
    del line[cap_index: len(line)]

  # Debug draw the line
  # draw_point_circles(line, group)
  # draw_point_path(line)
  # # centers = generate_centerpoints(line)
  # # draw_curved_path(line, centers, group)
  # return

  random.seed(seed)
  snake_points = build_snake.draw_snake_from_points(line, params, inflate_step)
  random.seed(seed)
  snake_points_spines = build_snake.draw_snake_from_points(line, params, inflate_step * params.spine_factor)

  # Do push
  build_push.push_lines(snake_points, params, seed, group)

  # Expand Boundary
  print_overwrite("Checking volume...")
  expand = ExpandingVolume()
  expand.add_lists(snake_points)
  # expand.add_lists(snake_points_spines)

  # Calculate scale
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)
  root_node = Node()
  root_node.transform.translate_point(offset)
  root_node.transform.scale(final_scale, final_scale)
  scaled_node = root_node.add_child()
  scaled_transform = scaled_node.transformation()
  scaled_points = scaled_transform.apply_to_point_arrays(snake_points)
  scaled_spines = scaled_transform.apply_to_point_arrays(snake_points_spines)

  # Debug draw original points
  if params.debug_draw_points:
    scaled_originals = scaled_transform.apply_to_point_array(line)
    draw_point_circles(scaled_originals, group)

  draw_boundary = try_get(params, 'debug_draw_boundary', False)
  rib_group = group
  spine_group = group

  if draw_boundary:
    group_red = open_group(GroupSettings(stroke=GroupColor.red, name="debug_red"), group)
    spine_group = open_group(GroupSettings(stroke=GroupColor.blue, name="debug_blue"), group)

  # Draw Result
  if params.draw_head:
    head_point = snake_points[0][0]
    draw_circ(head_point.x, head_point.y, 20, group)

  break_count = try_get(params, 'break_count', 0)
  break_loop = try_get(params, 'break_loop', 3)
  break_size = 5
  break_pos = Point(break_size + 2, svg_full().bottom() - break_size - 2)
  count_breaks = 0

  len_ribs = len(scaled_points)
  for i in range(1, len_ribs):
    print_overwrite(f"Drawing rib {pad_max(i + 1, len_ribs)}")
    if params.draw_ribs:
      rib = scaled_points[i]
      centers = generate_centerpoints(rib)
      draw_curved_path(rib, centers, rib_group)
    if params.draw_spine:
      spine = scaled_spines[i]
      centers = generate_centerpoints(spine)
      draw_curved_path(spine, centers, spine_group)

    if i > 0 and break_count > 0 and i % break_count == 0:
      count_breaks += 1
      for i in range(0, break_loop):
        draw_circ_point(break_pos, break_size, group)
      if draw_boundary:
        draw_circ_point(rib[0], 10, group_red)

  print_finish_overwite()

  if break_count > 0 and count_breaks > 0:
    print('Breaks:', count_breaks)

  print("Finished snake")

