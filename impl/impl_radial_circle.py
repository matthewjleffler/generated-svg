from lib import *


###
### Radial Circle Design
###


class BorderType(ReloadIntEnum):
  Empty = 0
  Circles = 1
  Starburst = 2

class RadialParams(TypedDict):
  draw_circles: bool
  draw_border: bool
  rotate_range: float
  ring_pad: float
  ring_weights: Weights[int]
  border_weights: Weights[BorderType]
  padding: int
  size_range: RangeInt
  size_pad: float
  origin_shuffle_range: float

  @classmethod
  def create(cls, defaults: Defaults) -> 'RadialParams':
    result: RadialParams = {
      'draw_circles': True,
      'draw_border': True,
      'rotate_range': pi / 10,
      'ring_pad': 5,
      'ring_weights': [
        (0, 5), (1, 2), (2, 1), (3, 0.5)
      ],
      'border_weights': [
        (BorderType.Empty, 5), (BorderType.Circles, 1), (BorderType.Starburst, 2)
      ],
      'padding': 0,
      'size_range': RangeInt(20, 350),
      'size_pad': 20,
      'origin_shuffle_range': 0,
    }
    return apply_defaults(result, defaults)


def _point(center_x:float, center_y:float, rad:float, dist:float) -> Point:
  return Point(round(_cos_point(center_x, rad, dist), 2),
               round(_sin_point(center_y, rad, dist), 2))

def _cos_point(center:float, rads:float, dist:float) -> float:
  return center + cos(rads) * dist

def _sin_point(center:float, rads:float, dist:float) -> float:
  return center + sin(rads) * dist

def _draw_circle(
  x:float,
  y:float,
  rays:int,
  min_dist:float,
  max_dist:float,
  points:List[Point],
  params:RadialParams):

  # Create original rough line
  rough_points: List[Point] = []
  rough_points.append(_point(x, y, 0, min_dist))
  rough_points.append(_point(x, y, 0, max_dist))

  # Draw rough line
  # draw_point_circles(rough_points)
  # draw_point_path(rough_points)

  # Subdivide
  subdivisions = floor(max_dist / 10)
  if subdivisions % 2 == 1:
    subdivisions += 1
  subdivided = subdivide_point_path(rough_points, RangeInt(subdivisions, subdivisions))

  # Adjust control points
  for i in range(1, len(subdivided), 2):
    sub = subdivided[i].subtract_floats_copy(x, y)
    rot = rand_float(-params['rotate_range'], params['rotate_range'])
    fine = sub.rotate_copy(rot)
    subdivided[i] = Point(x + fine.x, y + fine.y)

  # Draw subdivided line
  # draw_point_circles(subdivided)
  # draw_point_path(subdivided)

  # Copy by number of rays
  for i in range(0, rays):
    final: List[Point] = []

    rot = (i / rays) * pi * 2
    for sub in subdivided:
      rotated = sub.subtract_floats_copy(x, y)
      rotated = rotated.rotate_copy(rot)
      final.append(Point(round(x + rotated.x, 2), round(y + rotated.y, 2)))

    # Draw rotated lines
    points.append(final)

def _add_border(x:float, y:float, size_h:float, params:RadialParams, group: Group):
  ring_count = rand_weight(params['ring_weights'])

  if params['draw_border']:
    for i in range(0, ring_count):
      draw_circ(x, y, size_h + params['ring_pad'] + params['ring_pad'] * i, group)

  ring_buffer = params['ring_pad'] + params['ring_pad'] * (ring_count + 1)

  border = rand_weight(params['border_weights'])
  if border == BorderType.Empty or not params['draw_border']:
    return
  elif border == BorderType.Circles:
    draw_ring_of_circles(floor(size_h / 3), x, y, size_h + ring_buffer, 5, group)
  elif border == BorderType.Starburst:
    draw_sunburst(floor(size_h / 3), x, y, size_h + ring_buffer, 5, group)

def draw_radial_circles(params:RadialParams, group:Group):
  reload_libs(globals())

  # draw_border(group)

  # Rough path
  pad_rect = svg_safe().shrink_copy(params['padding'])

  # Generate points and control points
  points: List[List[Point]] = []

  size_h = params['size_range'].rand()
  size = size_h + params['size_pad']
  size_d = size * 2

  col_max = floor(pad_rect.w / size_d)
  row_max = floor(pad_rect.h / size_d)

  offset_x = (svg_safe().w - (col_max * size_d)) / 2
  offset_y = (svg_safe().h - size / 2 - (row_max * size_d * .85)) / 2

  # Calculate circles and draw borders
  group_blue = open_group(GroupSettings(stroke=GroupColor.blue), group)
  for row in range(0, row_max):
    y = offset_y + pad_rect.y + size + (size_d * .85) * row
    for col in range(0, col_max):
      x = offset_x + pad_rect.x + size + size_d * col
      if row % 2 == 1:
        if col == col_max - 1:
          continue
        x += size
      change_x = rand_float(-params['origin_shuffle_range'], params['origin_shuffle_range'])
      change_y = rand_float(-params['origin_shuffle_range'], params['origin_shuffle_range'])
      x += change_x
      y += change_y
      _draw_circle(x, y, floor(size_h / 2), 10, size_h, points, params)
      _add_border(x, y, size_h, params, group_blue)

  # Draw points
  for point_array in points:
    # draw_point_circles(point_array, group)
    # draw_point_path(point_array, group)

    start = point_array[0]
    path = "M{} {}".format(start.x, start.y)
    for i in range(1, len(point_array), 2):
      control = point_array[i]
      end = point_array[i + 1]
      path += "Q{} {} {} {}".format(control.x, control.y, end.x, end.y)

    if params['draw_circles']:
      draw_path(path, group)

