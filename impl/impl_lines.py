from lib import *
import drawing.build_push as build_push


###
### Lines
###

class LinesParams(TypedDict, build_push.PushOptions):
  draw: bool
  debug_draw_boundary: bool
  separation: int
  alternate_line_dir: bool
  subdivisions: int
  break_count: int
  break_loop: int

  @classmethod
  def create(cls, defaults: Defaults) -> 'LinesParams':
    result: LinesParams = {
      'draw': True,
      'debug_draw_boundary': True,

      'separation': 2,
      'alternate_line_dir': False,
      'subdivisions': 100,
      'break_count': 50,
      'break_loop': 3,

      # Push params
      'do_push': True,
      'push_settings': [
        { 'strength': 100 },
      ],
    }
    return apply_defaults(result, defaults)


def draw_lines(params: LinesParams, seed: int, group: Group):
  reload_libs(globals())

  pad = svg_safe().copy()
  pad_bottom = pad.bottom()
  debug_draw_boundary = params['debug_draw_boundary']

  # Draw safety border and page border
  if debug_draw_boundary:
    draw_border(group)

  sep_count = floor(pad.w / params['separation'])
  sep_spread = pad.w / sep_count

  lines: List[List[Point]] = []
  alternate = params['alternate_line_dir']
  for i in range(0, sep_count + 1):
    x = pad.x + i * sep_spread
    line = Line(Point(x, pad.y), Point(x, pad_bottom))
    if alternate and i % 2 != 0:
      line.reverse()
    lines.append(line.points())

  # for line in lines:
  #   draw_point_path(line, group)

  subdivided: List[List[Point]] = []
  subdivisions = params['subdivisions']
  subdivision_range = RangeInt(subdivisions, subdivisions)
  for line in lines:
    sub = subdivide_point_path(line, subdivision_range)
    subdivided.append(sub)

  build_push.push_lines(subdivided, params, seed, group)

  # Encapsulate
  expand = ExpandingVolume()
  expand.add_lists(subdivided)

  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)
  group_scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)
  if debug_draw_boundary:
    group_red = open_group(GroupSettings(stroke=GroupColor.red), group_scaled)

  break_count = params['break_count']
  break_loop = params['break_loop']
  break_size = 5
  break_pos = Point((break_size - offset.x) / final_scale, (svg_full().bottom() - break_size * 2 - offset.y) / final_scale)
  count_breaks = 0

  if params['draw']:
    for i in range(0, len(subdivided)):
      line = subdivided[i]
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, group_scaled)

      if i > 0 and break_count > 0 and i % break_count == 0:
        count_breaks += 1
        for i in range(0, break_loop):
          draw_circ_point(break_pos, break_size / final_scale, group_scaled)
        if debug_draw_boundary:
          draw_circ_point(line[0], 10, group_red)
