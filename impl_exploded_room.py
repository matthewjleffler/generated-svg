from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from typing import List

###
### Exploded Room Drawing
###

class ExplodedRoomParams(BaseParams):
  def __init__(self, defaults: Defaults) -> None:
    self.draw: bool = True
    self.slope: int = 100
    self.skew_height: RangeFloat = RangeFloat(0.1, 0.3)
    self.perspective_skew: RangeFloat = RangeFloat(0.2, 0.5)
    self.wall_width: RangeFloat = RangeFloat(0.1, 0.8)
    self.wall_inset_left: RangeFloat = RangeFloat(0.01, 0.1)
    self.wall_inset_right: RangeFloat = RangeFloat(0.01, 0.2)
    self.wall_bottom_inset: RangeFloat = RangeFloat(0.01, 0.4)
    self.row: RangeInt = RangeInt(1, 20)
    self.col: RangeInt = RangeInt(1, 30)
    self.height_adjust: RangeFloat = RangeFloat(-.2, .1)
    self.split_pad_x: RangeFloat = RangeFloat(-.05, .2)
    self.split_pad_y: RangeFloat = RangeInt(-10, 10)

    super().__init__(defaults)


def _offset_skew(skew:int, offset:Point, params: ExplodedRoomParams) -> Line:
  return Line(Point(offset.x, offset.y), Point(offset.x + skew, offset.y + params.slope))

def _skew_intersect(skew:int, offset:Point, target: Line, params: ExplodedRoomParams) -> Point:
  return line_intersection(_offset_skew(skew, offset, params), target)

def _horizontal_line(y: int) -> Line:
  return Line(Point(0, y), Point(100, y))

def _draw_clip_line(
    p0:Point,
    p1:Point,
    clip:List[shapely.geometry.Polygon],
    group: Group
):
  extra: List[Point] = []
  line = [p0, p1]
  for poly in clip:
    diff = poly_diff(line[0], line[1], poly)
    line = diff[0]
    for i in range(1, len(diff)):
      extra.append(diff[i])
    if len(line) < 1:
      break
  if len(line) > 0:
    clamp_point_list(1, line)
    draw_point_path(line, group)
  for ext in extra:
    _draw_clip_line(ext[0], ext[1], clip, group)

def _draw_clip_path(path: List[Point], clip:List[shapely.geometry.Polygon], group: Group):
  for i in range(0, len(path) - 1):
    _draw_clip_line(path[i], path[i + 1], clip, group)

def _create_room(
    skew:int,
    skew_height:int,
    rect:Rect,
    clip:List[shapely.geometry.Polygon],
    params:ExplodedRoomParams,
    group:Group = None
) -> shapely.geometry.Polygon:
  # Create top and bottom rings based on height
  bot_front_line = _horizontal_line(rect.bottom())
  bot_out_br_point = Point(rect.right(), rect.bottom())
  bot_out_tl_point = Point(rect.x, rect.bottom() - skew_height)
  bot_back_line = _horizontal_line(bot_out_tl_point.y)
  bot_out_bl_point = _skew_intersect(skew, bot_out_tl_point, bot_front_line, params)
  bot_out_tr_point = _skew_intersect(skew, bot_out_br_point, bot_back_line, params)

  height = bot_out_tl_point.subtract_copy(Point(rect.x, rect.y)).length()
  wall_bottom_inset = params.wall_bottom_inset.rand() * height

  # Collect rings in point lines
  bot_out_path = [bot_out_tl_point, bot_out_tr_point, bot_out_br_point, bot_out_bl_point, bot_out_tl_point]
  mid_out_path = offest_point_path(bot_out_path, Point(0, -wall_bottom_inset))
  top_out_path = offest_point_path(bot_out_path, Point(0, -height))

  # Create inner rings
  bot_center_x = (bot_out_tl_point.x + bot_out_tr_point.x + bot_out_br_point.x + bot_out_bl_point.x) / 4
  bot_center_y = (bot_out_tl_point.y + bot_out_tr_point.y + bot_out_br_point.y + bot_out_bl_point.y) / 4
  bot_center = Point(bot_center_x, bot_center_y)

  bot_in_tl_point = bot_center.subtract_copy(bot_out_tl_point)
  wall_width = params.wall_width.rand() * bot_in_tl_point.length()
  bot_in_tl_point.normalize()
  bot_in_tl_point.multiply(wall_width)
  bot_in_tl_point.add(bot_out_tl_point)
  bot_in_br_point = bot_center.subtract_copy(bot_out_br_point)
  bot_in_br_point.normalize()
  bot_in_br_point.multiply(wall_width)
  bot_in_br_point.add(bot_out_br_point)
  bot_in_back_line = _horizontal_line(bot_in_tl_point.y)
  bot_in_front_line = _horizontal_line(bot_in_br_point.y)
  bot_in_tr_point = _skew_intersect(skew, bot_in_br_point, bot_in_back_line, params)
  bot_in_bl_point = _skew_intersect(skew, bot_in_tl_point, bot_in_front_line, params)

  # Collect rings in point lines
  bot_in_path = [bot_in_tl_point, bot_in_tr_point, bot_in_br_point, bot_in_bl_point, bot_in_tl_point]
  mid_in_path = offest_point_path(bot_in_path, Point(0, -wall_bottom_inset))
  top_in_path = offest_point_path(bot_in_path, Point(0, -height))

  # Create inset points
  wall_left_len = bot_out_bl_point.subtract_copy(bot_out_tl_point).length()
  wall_right_len = bot_out_bl_point.subtract_copy(bot_out_br_point).length()
  wall_inset_left = wall_left_len * params.wall_inset_left.rand()
  wall_inset_right = wall_right_len * params.wall_inset_right.rand()
  top_left_inset_line = _horizontal_line(top_in_path[0].y + wall_inset_left)
  top_left_inset_in = _skew_intersect(skew, top_in_path[0], top_left_inset_line, params)
  top_left_inset_out = _skew_intersect(skew, top_out_path[0], top_left_inset_line, params)

  top_right_inset_line = _horizontal_line(top_out_path[2].y)
  top_right_inset_in = top_in_path[2].add_copy(Point(-wall_inset_right, 0))
  top_right_inset_out = _skew_intersect(skew, top_right_inset_in, top_right_inset_line, params)

  mid_left_inset_line = _horizontal_line(mid_in_path[0].y + wall_inset_left)
  mid_left_inset_in = _skew_intersect(skew, mid_in_path[0], mid_left_inset_line, params)
  mid_left_inset_out = _skew_intersect(skew, mid_out_path[0], mid_left_inset_line, params)

  mid_right_inset_line = _horizontal_line(mid_out_path[2].y)
  mid_right_inset_in = mid_in_path[2].add_copy(Point(-wall_inset_right, 0))
  mid_right_inset_out = _skew_intersect(skew, mid_right_inset_in, mid_right_inset_line, params)

  left_inset: List[Point] = [top_left_inset_out, top_left_inset_in, mid_left_inset_in, mid_left_inset_out]
  right_inset: List[Point] = [top_right_inset_in, top_right_inset_out, mid_right_inset_out, mid_right_inset_in]

  # Outer rim
  rim = to_polygon([
    top_out_path[0],
    top_out_path[1],
    top_out_path[2],
    bot_out_path[2],
    bot_out_path[3],
    bot_out_path[0],
  ],[[
    top_in_path[0],
    top_in_path[1],
    top_in_path[2],
    right_inset[0],
    right_inset[3],
    mid_in_path[3],
    left_inset[2],
    left_inset[1],
  ]])

  outer = to_polygon([
    top_out_path[0],
    top_out_path[1],
    top_out_path[2],
    bot_out_path[2],
    bot_out_path[3],
    bot_out_path[0]
  ])

  # Find which clips might affect this rim
  affected = []
  affected_all = [rim]
  for poly in clip:
    if outer.intersects(poly):
      affected.append(poly)
      affected_all.append(poly)

  # Draw result
  if params.draw:

    # Outer rim
    _draw_clip_path([
      top_out_path[0],
      top_out_path[1],
      top_out_path[2],
      bot_out_path[2],
      bot_out_path[3],
      bot_out_path[0],
      top_out_path[0],
    ], affected, group)

    # Inner inset
    _draw_clip_path([
      top_out_path[0],
      left_inset[0],
      left_inset[1],
      top_in_path[0],
      top_in_path[1],
      top_in_path[2],
      right_inset[0],
      right_inset[1],
      top_out_path[2],
    ], affected, group)

    # Front outer inset rim
    _draw_clip_path([
      right_inset[1],
      right_inset[2],
      mid_out_path[3],
      left_inset[3],
      left_inset[0],
    ], affected, group)

    # Left inset rim
    _draw_clip_path([
      left_inset[1],
      left_inset[2],
      left_inset[3],
    ], affected, group)

    # Front inner inset rim
    _draw_clip_path([
      left_inset[2],
      mid_in_path[3],
      right_inset[3],
      right_inset[2],
    ], affected, group)

    # Right inset rim
    _draw_clip_path([
      right_inset[3],
      right_inset[0],
    ], affected, group)

    # Back corners
    _draw_clip_line(top_in_path[1], bot_in_path[1], affected_all, group)
    _draw_clip_line(bot_in_path[0], bot_in_path[1], affected_all, group)
    _draw_clip_line(bot_in_path[2], bot_in_path[1], affected_all, group)

    # Front edge
    _draw_clip_line(mid_out_path[3], bot_out_path[3], affected, group)

    # Return new clip
    return outer


def draw_exploded_room(params: ExplodedRoomParams, group:Group):
  # draw_border(group)

  pad = svg_safe().copy()
  row = params.row.rand()
  col = params.col.rand()

  orig_width = pad.w / col

  split_pad_x = orig_width * params.split_pad_x.rand()
  if split_pad_x > 0:
    split_pad_x = max(split_pad_x, 10)
  split_pad_y = params.split_pad_y.rand()
  width = (pad.w - (col - 1) * split_pad_x) / col
  height = (pad.h - (row - 1) * split_pad_y) / row
  skew = params.perspective_skew.rand() * width
  skew_height = params.skew_height.rand() * height

  clip_list: List[shapely.geometry.Polygon] = []
  row_list = reversed(list(range(0, row)))
  for r in row_list:
    for c in range(0, col):
      extra_height = height * params.height_adjust.rand()
      top = pad.y + (height + split_pad_y) * r - extra_height
      clamped_top = max(pad.y, top)
      diff = clamped_top - top

      rect = Rect(pad.x + (width + split_pad_x) * c, clamped_top, width, height + extra_height + diff)
      room_clip = _create_room(skew, skew_height, rect, clip_list, params, group)

      # Add room to new clip shape
      did_combine = False
      for c in range(0, len(clip_list)):
        clip = clip_list[c]
        if clip.intersects(room_clip):
          combined = shapely.unary_union([clip, room_clip])
          clip_list[c] = combined
          did_combine = True
          break
      if not did_combine:
        clip_list.append(room_clip)

