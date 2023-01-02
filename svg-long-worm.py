import lib
import random
import math
from enum import IntEnum
from typing import List

# TODO highlight stroke types?
# TODO text paths?

class Position:
  def __init__(self, x, y, size) -> None:
    self.x = x
    self.y = y
    self.size = size

  def point(self) -> lib.Point:
    return lib.Point(self.x, self.y)


# Setup variables
step_dist = 5 # How far (roughly) between steps
circle = True # Render circles or squares
clamp_point = 0 # Clamping the line point positions
clamp_size = 0 # Clamping the rendering positions
size_digits = 2 # How many digits to round the radius size to

# Layout generation
min_peaks = 3
max_peaks = 3
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

# Init variables
points:List[lib.Point] = [] # Line points
centers:List[lib.Point] = [] # Line centers for bezier curves
positions:List[Position] = [] # Final render positions


class HighlightType(IntEnum):
  Circle = 0
  DoubleRing = 1,
  SunRing = 2,

  End = 3,


def init():
  global points, centers, positions
  points = []
  centers = []
  positions = []


# Round line points (pre-curve)
def round_line(value):
  if clamp_point == 0:
    return round(value, 0)
  return round(value / clamp_point, 0) * clamp_point


# Round render positions
def round_position(value):
  if clamp_size == 0:
    return round(value, 0)
  return round(value / clamp_size, 0) * clamp_size


def clamp(val, minv, maxv):
  return max(min(val, maxv), minv)


def add_nondup_position(x, y, size, array):
  for item in array:
    if item.x == x and item.y == y and item.size == size:
      return
  array.append(Position(x, y, size))


def step_along_quadratic(start, end, control, t):
  x = (1 - t) * (1 - t) * start.x + 2 * (1 - t) * t * control.x + t * t * end.x
  y = (1 - t) * (1 - t) * start.y + 2 * (1 - t) * t * control.y + t * t * end.y
  return lib.Point(x, y)


def add_points_along_line(p0, p1, size, next_size):
  vector = p1.subtract(p0)
  length = vector.length()
  vector.normalize()

  copy = vector.multiply_copy(step_dist)
  copy_len = copy.length()
  while copy_len < length:
    step_size = lib.ease_in_out_quad(copy_len, size, next_size - size, length)
    # step_size = round(lib.lerp(size, next_size, copy_len / length), size_digits)
    if circle:
      add_nondup_position(round_position(p0.x + copy.x), round_position(p0.y + copy.y), step_size, positions)
    else:
      x = p0.x + copy.x - step_size
      y = p0.y + copy.y - step_size
      add_nondup_position(round_position(x), round_position(y), step_size * 2, positions)
    copy = vector.multiply_copy(copy_len + step_dist)
    copy_len = copy.length()

  if circle:
    add_nondup_position(round_position(p1.x), round_position(p1.y), next_size, positions)
  else:
    x = p1.x - next_size
    y = p1.y - next_size
    add_nondup_position(round_position(x), round_position(y), next_size * 2, positions)


def add_points_along_curve(p0, p1, control, size, next_size):
  vector = p1.subtract(p0)
  length = vector.length() * 1.1
  steps = math.floor(length / step_dist)

  for i in range(0, steps):
    t = i / steps
    point = step_along_quadratic(p0, p1, control, t)

    step_size = round(lib.ease_in_out_quad(t, size, next_size - size, 1), size_digits)
    # step_size = lib.lerp(size, next_size, t)

    if circle:
      add_nondup_position(round_position(point.x), round_position(point.y), step_size, positions)
    else:
      x = point.x - step_size
      y = point.y - step_size
      add_nondup_position(round_position(x), round_position(y), step_size * 2, positions)

  # Finish with final point
  if circle:
    add_nondup_position(round_position(p1.x), round_position(p1.y), next_size, positions)
  else:
    x = p1.x - next_size
    y = p1.y - next_size
    add_nondup_position(round_position(x), round_position(y), next_size * 2, positions)


def draw_worm_path(draw):
  point = centers[0]
  path = "M{} {} L{} {}".format(points[0].x, points[0].y, point.x, point.y)

  for i in range(1, len(centers)):
    if i == len(points) -1:
      break
    point = centers[i]
    control = points[i]
    path += " Q{} {} {} {}".format(control.x, control.y, point.x, point.y)

  final = points[len(points) - 1]
  path += " L{} {}".format(final.x, final.y)

  # Draw curved line
  # lib.path(path)

  # Draw start circle
  if circle:
    add_nondup_position(round_position(points[0].x), round_position(points[0].y), size_end, positions)
  else:
    x = points[0].x - size_end
    y = points[0].y - size_end
    add_nondup_position(round_position(x), round_position(y), size_end * 2, positions)
  size = size_end
  next_size = 0

  # Add positions
  for i in range(1, len(points) + 1):
    next_size = random.randrange(size_min, size_max)
    if i == len(points):
      next_size = size_end

    if i == 1:
      # Draw straight line in beginning
      p0 = points[i - 1]
      p1 = centers[i - 1]
      add_points_along_line(p0, p1, size, next_size)
    elif i == len(points):
      # Draw straight line at end
      p0 = centers[i - 2]
      p1 = points[i - 1]
      add_points_along_line(p0, p1, size, next_size)
    else:
      # Draw along quadratic bezier curve for each other step
      p0 = centers[i - 2]
      p1 = centers[i - 1]
      control = points[i - 1]
      add_points_along_curve(p0, p1, control, size, next_size)

    size = next_size

  # Draw actual items created in last loop
  if draw:
    for pos in positions:
      if circle:
        lib.circ(pos.x, pos.y, pos.size)
      else:
        lib.rect(pos.x, pos.y, pos.size, pos.size)


def check_point_consumed(position:Position, consumed_highlights:List[Position]):
  point = position.point()
  for consumed in consumed_highlights:
    vec = consumed.point()
    vec = vec.subtract(point)

    len = vec.length()
    size = position.size + consumed.size + consumed_check_radius + highlight_padding * 2
    if len < size:
      return True
  return False


def pick_valid_highlight(available_highlights, consumed_highlights):
  while True:
    index = random.randint(0, len(available_highlights) - 1)
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


def draw_worm_highlights(draw):
  lib.open_group("stroke=\"blue\"")

  start = points[0]
  end = points[-1]

  # Draw rings
  if draw:
    lib.ring_of_circles(highlight_end_points, start.x, start.y, highlight_end_circle_radius, highlight_end_point_radius)
    lib.sunburst(highlight_end_points, end.x, end.y, highlight_end_circle_radius, 10)
    # lib.ring_of_circles(highlight_end_points, end.x, end.y, highlight_end_circle_radius, highlight_end_point_radius)

  consumed_highlights = []
  consumed_highlights.append(Position(start.x, start.y, highlight_end_circle_radius))
  consumed_highlights.append(Position(end.x, end.y, highlight_end_circle_radius))

  available_highlights = []
  for i in range(0, len(positions)):
    available_highlights.append(i)

  # highlight_size = size_max + 10
  highlight_count = random.randint(min_highlights, max_highlights)

  connect_next = False
  last = lib.Point(0,0)

  while highlight_count > 0:
    # Pick valid highlight
    point = pick_valid_highlight(available_highlights, consumed_highlights)
    if point is None:
      return # Ran out of points

    # Pick random highlight type
    highlight_index = random.randint(0, int(HighlightType.End - 1))
    highlight_type = HighlightType(highlight_index)

    highlight_count -= 1
    highlight_size = point.size + highlight_padding

    if draw:
      if connect_next:
        lib.path("M {} {} L{} {}".format(last.x, last.y, point.x, point.y))

      if highlight_type == HighlightType.Circle:
        lib.circ(point.x, point.y, highlight_size)
      elif highlight_type == HighlightType.DoubleRing:
        lib.circ(point.x, point.y, highlight_size)
        lib.circ(point.x, point.y, highlight_size + 10)
      elif highlight_type == HighlightType.SunRing:
        lib.circ(point.x, point.y, highlight_size)
        lib.sunburst(20, point.x, point.y, highlight_size + 10, 10)

    last = point
    connect_next = random.randint(0, 3) == 0

  lib.close_group()


def loop(draw_worm, draw_highlight):
  # lib.border()

  init()

  # Variables
  peaks = random.randint(min_peaks, max_peaks)
  top_first = random.randint(0, 1) == 0

  # Build outline
  padding = 100
  top = lib.svg_safe.y + padding
  bottom = lib.svg_safe.bottom() - padding
  center_y = lib.svg_full.h / 2
  left = lib.svg_safe.x + padding
  right = lib.svg_safe.right() - padding
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
  rough_points = []
  rough_points.append(lib.Point(left, center_y))
  for i in range(0, peaks):
    rough_points.append(lib.Point(left + space * (i + 1), first))
    rough_points.append(lib.Point(left + space * (i + 1), second))
  rough_points.append(lib.Point(right, center_y))

  # Shuffle rough points
  for point in rough_points:
    change_x =  random.randrange(-shuffle_large_max_x, shuffle_large_max_x)
    change_y = random.randrange(-shuffle_large_max_y, shuffle_large_max_y)
    point.x = clamp(point.x + change_x, left, right)
    point.y = clamp(point.y + change_y, top, bottom)

  # Draw rough points
  # last = rough_points[0]
  # path = "M{} {}".format(last.x, last.y)
  # for i in range(1, len(rough_points)):
  #   point = rough_points[i]
  #   path += " L{} {}".format(point.x, point.y)
  # lib.path(path)

  # Subdivide rough path
  last = rough_points[0]
  points.append(rough_points[0])

  for i in range(1, len(rough_points)):
    point = rough_points[i]
    vector = point.subtract(last)
    length = vector.length()

    subdivisions = random.randint(rough_subdivisions_min, rough_subdivisions_max)
    if i == 1 or i == len(rough_points) - 1:
      subdivisions = 1

    sub_length = length / subdivisions
    vector.normalize()
    vector.multiply(sub_length)

    x = last.x
    y = last.y
    lib.add_nondup_point(round(x, 0), round(y, 0), points)
    for _ in range(0, subdivisions):
      x += vector.x
      y += vector.y
      lib.add_nondup_point(round(x, 0), round(y, 0), points)
    last = point

  # Shuffle subdivided path
  for point in points:
    change_x = random.randrange(-shuffle_small_max_x, shuffle_small_max_x)
    change_y = random.randrange(-shuffle_small_max_y, shuffle_small_max_y)
    point.x += change_x
    point.y += change_y

  # Draw subdivided points
  # last = points[0]
  # path = "M{} {}".format(last.x, last.y)
  # for i in range(1, len(points)):
  #   point = points[i]
  #   path += " L{} {}".format(point.x, point.y)
  # lib.path(path)

  # Generate centerpoints
  last = points[0]
  for i in range(1, len(points)):
    point = points[i]

    # Calculuate center point
    vector = point.subtract(last)
    length = vector.length()
    vector.normalize()
    vector.multiply(length / 2)

    center_x = last.x + vector.x
    center_y = last.y + vector.y
    centers.append(lib.Point(center_x, center_y))

    # lib.circ(center_x, center_y, 5)

    last = point

  draw_worm_path(draw_worm)
  draw_worm_highlights(draw_highlight)


def loop_combined():
  loop(True, True)

def loop_worm():
  loop(True, False)

def loop_highlight():
  loop(False, True)


seed = 0
test = True
image_size = lib.SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = lib.main(
    "long-worm-combined",
    test,
    seed,
    image_size,
    loop_combined
  )

  lib.main(
    "long-worm-worm",
    test,
    mainseed,
    image_size,
    loop_worm
  )

  lib.main(
    "long-worm-highlight",
    test,
    mainseed,
    image_size,
    loop_highlight
  )

