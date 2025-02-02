from lib import *
import drawing.build_push as build_push


###
### Lines
###

class LinesParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.debug_draw_boundary: bool = True

    self.separation = 2
    self.alternate_line_dir = False
    self.subdivisions = 100
    self.break_count = 50

    # Push params
    self.do_push: bool = True
    self.push_settings = [
      create({ 'strength': 100 }),
    ]

    super().__init__(defaults)


def draw_lines(params: LinesParams, seed: int, group: Group):
  reload_libs(globals())

  pad = svg_safe().copy()
  pad_bottom = pad.bottom()

  # Draw safety border and page border
  if params.debug_draw_boundary:
    draw_border(group)

  sep_count = floor(pad.w / params.separation)
  sep_spread = pad.w / sep_count

  lines: List[List[Point]] = []
  for i in range(0, sep_count + 1):
    x = pad.x + i * sep_spread
    line = Line(Point(x, pad.y), Point(x, pad_bottom))
    if params.alternate_line_dir and i % 2 != 0:
      line.reverse()
    lines.append(line.points())

  # for line in lines:
  #   draw_point_path(line, group)

  subdivided: List[List[Point]] = []
  subdivision_range = RangeInt(params.subdivisions, params.subdivisions)
  for line in lines:
    sub = subdivide_point_path(line, subdivision_range)
    subdivided.append(sub)

  build_push.push_lines(subdivided, params, seed, group)

  # Encapsulate
  expand = ExpandingVolume()
  expand.add_lists(subdivided)

  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad)
  group_scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)
  if params.debug_draw_boundary:
    group_red = open_group(GroupSettings(stroke=GroupColor.red), group_scaled)

  break_count = try_get(params, 'break_count', 0)
  break_loop = try_get(params, 'break_loop', 3)
  break_size = 5
  break_pos = Point((break_size - offset.x) / final_scale, (svg_full().bottom() - break_size * 2 - offset.y) / final_scale)
  count_breaks = 0

  if params.draw:
    for i in range(0, len(subdivided)):
      line = subdivided[i]
      centers = generate_centerpoints(line)
      draw_curved_path(line, centers, group_scaled)

      if i > 0 and break_count > 0 and i % break_count == 0:
        count_breaks += 1
        for i in range(0, break_loop):
          draw_circ_point(break_pos, break_size / final_scale, group_scaled)
        if params.debug_draw_boundary:
          draw_circ_point(line[0], 10, group_red)
