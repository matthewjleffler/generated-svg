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


class SnakeParams(
  TypedDict,
  build_snake.SnakeOptions,
  build_maze.MazeOptions,
  build_push.PushOptions,
  build_triangle.TriangleOptions,
):
  draw: bool
  debug_draw_boundary: bool
  debug_draw_points: bool
  cell_size: int
  line_type: _SnakeType
  spine_factor: float
  do_cap: bool
  cap_percent: RangeFloat

  @classmethod
  def create(cls, defaults: Defaults) -> 'SnakeParams':
    result: SnakeParams = {
      'draw': True,
      'debug_draw_boundary': True,
      'debug_draw_points': False,
      'cell_size': 100,
      'line_type': _SnakeType.maze,
      'spine_factor': .15,
      'do_cap': False,
      'cap_percent': RangeFloat(.5, .99),

      # Snake options
      'draw_spine': False,
      'draw_head': False,
      'draw_ribs': True,
      'step_dist': 1,
      'do_inflate': False,
      'inflate_factor': 1,
      'end_falloff': .15,
      'do_average': True,
      'smoothing_range': 30,
      'smoothing_steps': 1,
      'do_inflate_corners': True,
      'inflate_corner_factor': 2,
      'final_average_weight': 2,
      'do_rib_shuffle': True,
      'rib_shuffle_amount': RangeFloat(.05, .5),
      'break_count': 200,
      'break_loop': 3,
      'original_ribs': False,
      'rib_range': RangeInt(3, 10),

      # Maze options
      'close_path': False,
      'do_inset': False,

      # Push options
      'do_push': False,
      'push_settings': [
        { 'strength': 10, 'strength_octave': 70, 'rotation_octave': 5 },
        { 'strength': 100, 'strength_octave': 2.5 },
      ],

      # Triangle options
      'triangle_step_size': 100,
    }
    return apply_defaults(result, defaults)


def draw_snake(params: SnakeParams, group: Group, seed: int):
  reload_libs(globals())

  pad = svg_safe().copy()

  # Draw safety border and page border
  if params['debug_draw_boundary']:
    draw_border(group)

  # Get line type
  if params['line_type'] == _SnakeType.maze:
    maze_size = build_maze.MazeSize(params['cell_size'], pad)

    # Make maze
    line: List[Point] = build_maze.make_maze_line(maze_size, params)
    if len(line) < 1:
      print('0 length maze')
      return
    inflate_step = max(int(min(maze_size.half_w / 2, maze_size.half_h / 2)), 5)

  elif params['line_type'] == _SnakeType.triangle:
    triangle_result = build_triangle.create_triangle_lines(pad, params)
    line = triangle_result.triangle_points
    inflate_step = max(int(params['triangle_step_size'] / 4), 5)

  # Re-init randomness after maze
  random.seed(seed)

  # Cap line
  cap_percent = params['cap_percent'].rand()
  cap_index = floor(len(line) * cap_percent)
  if params['do_cap']:
    del line[cap_index: len(line)]

  random.seed(seed)
  snake_points = build_snake.draw_snake_from_points(line, params, inflate_step)
  random.seed(seed)
  snake_points_spines = build_snake.draw_snake_from_points(line, params, inflate_step * params['spine_factor'])

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
  if params['debug_draw_points']:
    scaled_originals = scaled_transform.apply_to_point_array(line)
    draw_point_circles(scaled_originals, group)

  draw_boundary = params['debug_draw_boundary']
  rib_group = group
  spine_group = group

  if draw_boundary:
    group_red = open_group(GroupSettings(stroke=GroupColor.red, name="debug_red"), group)
    spine_group = open_group(GroupSettings(stroke=GroupColor.blue, name="debug_blue"), group)

  # Draw Result
  if params['draw_head']:
    head_point = snake_points[0][0]
    draw_circ(head_point.x, head_point.y, 20, group)

  break_count = params['break_count']
  break_loop = params['break_loop']
  break_size = 5
  break_pos = Point(break_size + 2, svg_full().bottom() - break_size - 2)
  count_breaks = 0

  len_ribs = len(scaled_points)
  for i in range(1, len_ribs):
    print_overwrite(f"Drawing rib {pad_max(i + 1, len_ribs)}")
    if params['draw_ribs']:
      rib = scaled_points[i]
      centers = generate_centerpoints(rib)
      draw_curved_path(rib, centers, rib_group)
    if params['draw_spine']:
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

