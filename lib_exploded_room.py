from lib import *
from lib_math import *
from lib_path import *
from lib_poly import *
from typing import List

###
### Exploded Room Drawing
###

class ExplodedRoomParams:
  def __init__(self) -> None:
    self.draw: bool = True
    self.slope: int = 100
    self.perspective_skew: RangeFloat = RangeFloat(0.1, 0.3)
    self.height: RangeFloat = RangeFloat(0.5, 0.8)
    self.wall_width: RangeFloat = RangeFloat(0.1, 0.8)
    self.wall_inset_left: RangeFloat = RangeFloat(0.01, 0.1)
    self.wall_inset_right: RangeFloat = RangeFloat(0.01, 0.2)
    self.wall_bottom_inset: RangeFloat = RangeFloat(0.01, 0.4)
    self.row: RangeInt = RangeInt(1, 30)
    self.col: RangeInt = RangeInt(1, 40)
    self.split_pad: RangeInt = RangeInt(5, 10)


def _offset_skew(skew:int, offset:Point, params: ExplodedRoomParams) -> Line:
  return Line(Point(offset.x, offset.y), Point(offset.x + skew, offset.y + params.slope))

def _skew_intersect(skew:int, offset:Point, target: Line, params: ExplodedRoomParams) -> Point:
  return line_intersection(_offset_skew(skew, offset, params), target)

def _horizontal_line(y: int) -> Line:
  return Line(Point(0, y), Point(100, y))

def _draw_room(skew:int, common_height:float, rect:Rect, params:ExplodedRoomParams, group:Group = None):
  # Randomize start
  height = common_height * rect.h
  wall_bottom_inset = params.wall_bottom_inset.rand() * height

  # Create initial lines
  top_out_back_line = _horizontal_line(rect.y)
  bot_out_front_line = _horizontal_line(rect.bottom())
  bot_out_back_line = _horizontal_line(rect.y + height)

  # Create top and bottom rings based on height
  top_out_tl_point = Point(rect.x, rect.y)
  top_out_br_point = Point(rect.right(), rect.bottom() - height)
  top_out_tr_point = _skew_intersect(skew, top_out_br_point, top_out_back_line, params)
  bot_out_tl_point = Point(rect.x, rect.y + height)
  bot_out_br_point = Point(rect.right(), rect.bottom())
  bot_out_bl_point = _skew_intersect(skew, bot_out_tl_point, bot_out_front_line, params)
  top_out_bl_point = bot_out_bl_point.add_copy(Point(0, -height))
  bot_out_tr_point = _skew_intersect(skew, bot_out_br_point, bot_out_back_line, params)

  # Collect rings in point lines
  top_out_path = [top_out_tl_point, top_out_tr_point, top_out_br_point, top_out_bl_point, top_out_tl_point]
  bot_out_path = [bot_out_tl_point, bot_out_tr_point, bot_out_br_point, bot_out_bl_point, bot_out_tl_point]
  mid_out_path = offest_point_path(bot_out_path, Point(0, -wall_bottom_inset))

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
    top_right_inset_in,
    mid_right_inset_in,
    mid_in_path[3],
    mid_left_inset_in,
    top_left_inset_in,
  ]])

  # Clip corners
  try:
    back_corner = poly_diff(top_in_path[1], bot_in_path[1], rim)
    left_corner = poly_diff(bot_in_path[0], bot_in_path[1], rim)
    right_corner = poly_diff(bot_in_path[2], bot_in_path[1], rim)
  except:
    back_corner = []
    left_corner = []
    right_corner = []
    print("Failed")
    print(wall_inset_left)
    print(wall_left_len)
    draw_circ_point(bot_center, 5, group)

  # Draw result
  if params.draw:
    # Outer rim
    draw_point_path([
      top_out_path[0],
      top_out_path[1],
      top_out_path[2],
      bot_out_path[2],
      bot_out_path[3],
      bot_out_path[0],
      top_out_path[0],
    ], group)

    # Inner inset
    draw_point_path([
      top_out_path[0],
      top_left_inset_out,
      top_left_inset_in,
      top_in_path[0],
      top_in_path[1],
      top_in_path[2],
      top_right_inset_in,
      top_right_inset_out,
      top_out_path[2],
    ], group)

    # Front outer inset rim
    draw_point_path([
      top_right_inset_out,
      mid_right_inset_out,
      mid_out_path[3],
      mid_left_inset_out,
      top_left_inset_out,
    ], group)

    # Left inset rim
    draw_point_path([
      top_left_inset_in,
      mid_left_inset_in,
      mid_left_inset_out,
    ], group)

    # Front inner inset rim
    draw_point_path([
      mid_left_inset_in,
      mid_in_path[3],
      mid_right_inset_in,
      mid_right_inset_out,
    ], group)

    # Right inset rim
    draw_point_path([
      mid_right_inset_in,
      top_right_inset_in,
    ], group)

    # Back corners
    if len(back_corner) > 0:
      draw_point_path(back_corner, group)
    if len(left_corner) > 0:
      draw_point_path(left_corner, group)
    if len(right_corner) > 0:
      draw_point_path(right_corner, group)

    # Front edge
    draw_point_path([
      mid_out_path[3],
      bot_out_path[3],
    ], group)


def draw_exploded_room(params: ExplodedRoomParams, group:Group = None):
  # draw_border(group)

  safe = svg_safe()
  row = params.row.rand()
  col = params.col.rand()

  split_pad = params.split_pad.rand()
  width = (safe.w - (col - 1) * split_pad) / col
  height = (safe.h - (row - 1) * split_pad) / row
  skew = params.perspective_skew.rand() * width
  common_height = params.height.rand()

  for r in range(0 ,row):
    for c in range(0, col):
      rect = Rect(safe.x + (width + split_pad) * c, safe.y + (height + split_pad) * r, width, height)
      _draw_room(skew, common_height, rect, params, group)
