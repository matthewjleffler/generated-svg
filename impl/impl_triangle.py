from lib import *
import drawing.build_triangle as build_triangle
import drawing.build_push as build_push


###
### Triangle Design
###

class TriangleParams(
  TypedDict,
  build_triangle.TriangleOptions,
  build_push.PushOptions
):
  debug_draw_boundary: bool
  draw_triangles: bool
  draw_background: bool
  hatch_triangle: bool
  hatch_background: bool

  @classmethod
  def create(cls, defaults: Defaults) -> 'TriangleParams':
    result: TriangleParams = {
      'debug_draw_boundary': True,

      'draw_triangles': True,
      'draw_background': False,
      'hatch_triangle': False,
      'hatch_background': False,

      # Triangle options
      'triangle_step_size': 50,
      'triangle_rotate': False,
      'triangle_rotate_range': RangeFloat(0, 180),
      'triangle_do_shuffle': False,
      'triangle_shuffle_range': 100,
      'triangle_angle': 30,

      # Push options
      'do_push': True,
      'push_settings': [
        { 'strength': 100 },
      ],
    }
    return apply_defaults(result, defaults)


def draw_triangle(params:TriangleParams, seed: int, group:Group):
  reload_libs(globals())

  pad_rect = svg_safe().copy()

  result = build_triangle.create_triangle_lines(pad_rect, params)
  triangle_points = result.triangle_points
  top = result.top
  right = result.right
  left = result.left
  center = result.center

  # Draw triangle vertices
  # for i in range(0, len(triangle_points)):
  #   draw_circ_point(triangle_points[i], i + 1, group)

  # Separate edges into lines for later subdivision
  triangle_lines: List[List[Point]] = []
  for i in range(0, len(triangle_points) - 1):
    triangle_lines.append([triangle_points[i], triangle_points[i + 1]])

  # Find volume
  expand = ExpandingVolume(triangle_points)

  # Find how far to the left and right we need to draw
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad_rect)
  bg_width = (pad_rect.w / final_scale)

  # Draw background lines
  background_lines: List[List[Point]] = []
  bg_count = floor(bg_width / (params['triangle_step_size'] / 2))
  bg_sep = bg_width / bg_count
  line_left = Line(top, left)
  line_right = Line(top, right)
  for i in range(0, bg_count + 1):
    x = center.x - (bg_width / 2 ) + bg_sep * i
    line_current = Line(Point(x, top.y), Point(x, left.y))
    intersect_left = line_intersection(line_current, line_left)
    intersect_right = line_intersection(line_current, line_right)
    intersect_max = max(intersect_left.y, intersect_right.y)
    intersect_bottom = min(intersect_max - (params['triangle_step_size']), left.y)
    if intersect_bottom < top.y:
      continue
    line_current.p1.y = intersect_bottom
    if i % 2 == 0:
      line_current.reverse()
    background_lines.append(line_current.points())

  # Subdivide all lines and collect them
  subdivision_range = RangeInt(100, 100)
  if params['do_push']:
    for i in range(0, len(triangle_lines)):
      triangle_lines[i] = subdivide_point_path(triangle_lines[i], subdivision_range)
    for i in range(0, len(background_lines)):
      background_lines[i] = subdivide_point_path(background_lines[i], subdivision_range)
  build_push.push_lines(triangle_lines + background_lines, params, seed, group)

  # Re-encapsulate all the points and recaclulate scale
  expand.add_lists(triangle_lines)
  expand.add_lists(background_lines)
  (offset, final_scale) = scale_rect_to_fit(expand.to_rect(), pad_rect)

  # Draw points
  if params['draw_triangles']:
    group_scaled = open_group(GroupSettings(translatePoint=offset, scale=final_scale), group)

    if params['debug_draw_boundary']:
      draw_point_path([Point(pad_rect.center_x(), pad_rect.y), Point(pad_rect.center_x(), pad_rect.bottom())], group_scaled)
      draw_border(group)
      draw_rect_rect(pad_rect, group_scaled)

    hatch_params = HatchParams(RangeInt(20, 50), RangeInt(3, 5))

    if params['hatch_triangle']:
      # TODOML support for split versions?
      draw_point_path_hatched(triangle_points, hatch_params, group_scaled)
    else:
      for line in triangle_lines:
        centers = generate_centerpoints(line)
        draw_curved_path(line, centers, group_scaled)

    if params['draw_background']:
      for line in background_lines:
        if params['hatch_background']:
          draw_point_path_hatched(line, hatch_params, group_scaled)
        else:
          # draw_point_path(line, scaled)
          centers = generate_centerpoints(line)
          draw_curved_path(line, centers, group_scaled)
