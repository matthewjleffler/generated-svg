from lib import *
from text import *
from path import *
from enum import IntEnum
from typing import List


# Setup variables
step_dist = 5 # How far (roughly) between steps
circle = True # Render circles or squares

# Layout generation
min_peaks = 3
max_peaks = 7
shuffle_large_max_x = 80
shuffle_large_max_y = 100
shuffle_small_max_x = 30
shuffle_small_max_y = 30
rough_subdivisions_min = 1
rough_subdivisions_max = 10

# Worm circle sizes
size_end = 1
size_min = 5
size_max = 60

# Highlights
highlight_end_circle_radius = 30
highlight_end_points = 10
highlight_end_point_radius = 5

min_highlights = 3
max_highlights = 5

highlight_padding = 20
consumed_check_radius = 50


class HighlightType(IntEnum):
  Circle = 0
  DoubleRing = 1,
  SunRing = 2,

  End = 3,


def check_point_consumed(position:Position, consumed_highlights:List[Position]) -> bool:
  point = position.point()
  for consumed in consumed_highlights:
    vec = consumed.point()
    vec = vec.subtract_copy(point)

    len = vec.length()
    size = position.size + consumed.size + consumed_check_radius + highlight_padding * 2
    if len < size:
      return True
  return False


def pick_valid_highlight(available_highlights:List[int], consumed_highlights:List[Position], positions:List[Position]):
  while True:
    index = rand_int(0, len(available_highlights) - 1)
    index = available_highlights.pop(index)
    position = positions[index]

    consumed = check_point_consumed(position, consumed_highlights)
    if not consumed:
      # We're good, consume the point
      consumed_highlights.append(position)
      return position

    # Are we out of points?
    if len(available_highlights) < 1:
      return None


def draw_worm_highlights(draw:bool, positions:List[Position]):
  open_group("stroke=\"blue\"")

  start = positions[0]
  end = positions[-1]

  # Draw rings
  if draw:
    draw_ring_of_circles(highlight_end_points, start.x, start.y, highlight_end_circle_radius, highlight_end_point_radius)
    draw_sunburst(highlight_end_points, end.x, end.y, highlight_end_circle_radius, 10)
    # draw_ring_of_circles(highlight_end_points, end.x, end.y, highlight_end_circle_radius, highlight_end_point_radius)

  consumed_highlights = []
  consumed_highlights.append(Position(start.x, start.y, highlight_end_circle_radius))
  consumed_highlights.append(Position(end.x, end.y, highlight_end_circle_radius))

  available_highlights = []
  for i in range(0, len(positions)):
    available_highlights.append(i)

  # highlight_size = size_max + 10
  highlight_count = rand_int(min_highlights, max_highlights)

  connect_next = False
  last = Point(0,0)

  while highlight_count > 0:
    # Pick valid highlight
    point = pick_valid_highlight(available_highlights, consumed_highlights, positions)
    if point is None:
      return # Ran out of points

    num = 0
    if rand_int(0, 3) == 0:
      num = rand_int(200, 50000)

    # Pick random highlight type
    highlight_index = rand_int(0, int(HighlightType.End - 1))
    highlight_type = HighlightType(highlight_index)

    highlight_count -= 1
    highlight_size = point.size + highlight_padding

    if draw:
      if connect_next:
        draw_path("M {} {} L{} {}".format(last.x, last.y, point.x, point.y))

      if highlight_type == HighlightType.Circle:
        draw_circ(point.x, point.y, highlight_size)
      elif highlight_type == HighlightType.DoubleRing:
        draw_circ(point.x, point.y, highlight_size)
        draw_circ(point.x, point.y, highlight_size + 10)
      elif highlight_type == HighlightType.SunRing:
        draw_circ(point.x, point.y, highlight_size)
        draw_sunburst(20, point.x, point.y, highlight_size + 10, 10)

      if num > 0:
        open_group("transform=\"translate({},{}) scale(0.5,0.5)\""
          .format(point.x + highlight_size * 1.5, point.y))
        draw_text(0, 0, 10, str(num))
        close_group()

    last = point
    connect_next = rand_int(0, 3) == 0

  close_group()


def loop(draw_worm:bool, draw_highlight:bool):
  # draw_border()

  # Variables
  peaks = rand_int(min_peaks, max_peaks)
  top_first = rand_int(0, 1) == 0

  # Build outline
  padding = 100
  top = svg_safe().y + padding
  bottom = svg_safe().bottom() - padding
  center_y = svg_full().center_y()
  left = svg_safe().x + padding
  right = svg_safe().right() - padding
  width = right - left

  # Subdivide space
  space = width / (peaks + 1)

  # Pick direction of motion
  if top_first:
    first = top
    second = bottom
  else:
    first = bottom
    second = top

  # Pick rough points
  rough_points: List[Point] = []
  rough_points.append(Point(left, center_y))
  for i in range(0, peaks):
    rough_points.append(Point(left + space * (i + 1), first))
    rough_points.append(Point(left + space * (i + 1), second))
  rough_points.append(Point(right, center_y))

  # Shuffle rough points
  shuffle_points(shuffle_large_max_x, shuffle_large_max_y, rough_points)

  # Draw rough points
  # draw_point_path(rough_points)

  # Subdivide rough path
  points = subdivide_point_path(rough_points, rough_subdivisions_min, rough_subdivisions_max)

  # Shuffle subdivided path
  shuffle_points(shuffle_small_max_x, shuffle_small_max_y, points)

  # Draw subdivided points
  # path.draw_point_path(points)

  centers = generate_centerpoints(points)
  # path.draw_curved_path(points, centers)
  positions = generate_final_positions(points, centers, size_end, size_min, size_max, step_dist)

  # Draw actual items created in last loop
  if draw_worm:
    for pos in positions:
      if circle:
        draw_circ(pos.x, pos.y, pos.size)
      else:
        draw_rect(pos.x - pos.size, pos.y - pos.size, pos.size * 2, pos.size * 2)

  draw_worm_highlights(draw_highlight, positions)


def loop_combined():
  loop(True, True)

def loop_worm():
  loop(True, False)

def loop_highlight():
  loop(False, True)


seed = 0
test = True
image_size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("long-worm-combined", test, seed, image_size, loop_combined)
  main("long-worm-worm", test, mainseed, image_size, loop_worm)
  main("long-worm-highlight", test, mainseed, image_size, loop_highlight)

