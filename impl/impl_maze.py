from lib import *
import drawing.build_maze as build_maze
import drawing.build_push as build_push


###
### Infinite Maze
###

class DrawType(ReloadEnum):
  straight = 0
  curved = 1
  hatched = 2


class MazeParams(
  TypedDict,
  build_maze.MazeOptions,
  build_push.PushOptions
):
  draw: bool
  debug_draw_boundary: bool
  debug_push: bool
  draw_type: DrawType
  cell_size: int
  do_cap: bool
  cap_percent: RangeFloat
  cutout_range: float
  do_inset: bool
  draw_cutout: bool
  circle_inset: float
  do_shuffle: bool
  shuffle_range: RangeFloat

  @classmethod
  def create(cls, defaults: Defaults) -> 'MazeParams':
    result: MazeParams = {
      'draw': True,
      'debug_draw_boundary': True,
      'debug_push': False,
      'draw_type': DrawType.curved,
      'cell_size': 7,
      'do_cap': False,
      'cap_percent': RangeFloat(.8, .99),
      'cutout_range': 0,
      'draw_cutout': False,
      'circle_inset': 15,
      'do_shuffle': True,
      'shuffle_range': RangeFloat(0, .75),

      # MazeOptions
      'close_path': True,
      'do_inset': False,

      # PushOption
      'do_push': True,
      'push_settings': [
        { 'strength': 100 },
      ],
    }
    return apply_defaults(result, defaults)


def draw_maze(params: MazeParams, seed:int, group: Group):
  reload_libs(globals())

  pad = svg_safe().copy()

  # Draw safety border and page border
  if params['debug_draw_boundary']:
    draw_border(group)

  cell_size = params['cell_size']
  print("Cell size:", cell_size)

  # Make maze
  maze_size = build_maze.MazeSize(cell_size, pad, params['cutout_range'])
  line = build_maze.make_maze_line(maze_size, params)

  if len(line) < 1:
    print('0 length maze')
    return

  cap_index = floor(len(line) * params['cap_percent'].rand())
  if params['do_cap']:
    del line[cap_index: len(line)]

  print("Points:", len(line))

  # Shuffle
  for point in line:
    offset_x = params['shuffle_range'].rand() * maze_size.half_w
    offset_y = params['shuffle_range'].rand() * maze_size.half_h
    if params['do_shuffle']:
      point.add_floats(offset_x, offset_y)

  # Do push
  build_push.push_line(line, params, seed, group)

  # Scale output to fit safe area
  expand = ExpandingVolume()
  for point in line:
    expand.add(point)
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)

  # Draw the line
  group_scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)
  if params['debug_draw_boundary']:
    draw_rect_rect(pad, group_scaled)
  if params['draw']:
    if params['draw_type'] == DrawType.curved:
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, group_scaled)
    if params['draw_type'] == DrawType.straight:
      draw_point_path(line, group_scaled)
    if params['draw_type'] == DrawType.hatched:
      centers = generate_centerpoints(line)
      final = generate_final_points(line, centers, 1)
      draw_point_path_hatched(final, HatchParams(RangeInt(3, 10), RangeInt(1, 3)), group_scaled)

    if params['draw_cutout'] and maze_size.range_stamp > 0:
      center_x = pad.center_x()
      if maze_size.col % 2 == 0:
        center_x += maze_size.node_w
      center_y = pad.center_y()
      if maze_size.row % 2 == 0:
        center_y += maze_size.node_h

      circ_size_base = (maze_size.range_stamp * 2) * maze_size.node_w
      draw_circ(center_x, center_y, circ_size_base - params['circle_inset'] - (maze_size.node_w), group_scaled)
      draw_circ(center_x, center_y, circ_size_base - params['circle_inset'] - (maze_size.node_w * 2), group_scaled)
