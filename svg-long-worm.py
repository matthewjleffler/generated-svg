import lib
import random

clamp_point = 0
def clamp_line(value):
  if clamp_point == 0:
    return value
  return round(value / clamp_point, 0) * clamp_point


clamp_size = 0
def clamp(value):
  if clamp_size == 0:
    return value
  return round(value / clamp_size, 0) * clamp_size


class Position:
  def __init__(self, x, y, size) -> None:
    self.x = x
    self.y = y
    self.size = size


def add_nondup_position(x, y, size, array):
  for item in array:
    if item.x == x and item.y == y:
      return
  array.append(Position(x, y, size))


def loop():
  # lib.border()

  points = []
  down = True
  padding = 100
  jump_x_min = 5
  jump_x_max = 10
  jump_y_min = 100
  jump_y_max = 150

  size_min = 1
  size_max = 50

  step_dist = 5

  circle = True

  top = lib.svg_safe.y + padding
  bottom = lib.svg_safe.bottom() - padding

  last_x = clamp_line(lib.svg_safe.x + padding)
  safe_third = round(lib.svg_safe.h / 3, 0)
  last_y = clamp_line(random.randrange(lib.svg_safe.y + safe_third, lib.svg_safe.bottom() - safe_third))
  points.append(lib.Point(last_x, last_y))

  while last_x < lib.svg_safe.right() - padding:
    last_x += random.randrange(jump_x_min, jump_x_max)
    last_x = clamp_line(last_x)
    if down:
      new_y = last_y + random.randrange(jump_y_min, jump_y_max)
      if new_y > bottom:
        down = False
        new_y = last_y
    else:
      new_y = last_y - random.randrange(jump_y_min, jump_y_max)
      if new_y < top:
        down = True
        new_y = last_y

    last_y = clamp_line(new_y)
    lib.add_nondup_point(last_x, last_y, points)

  path = ""
  for i in range(len(points)):
    point = points[i]
    if i == 0:
      path += "M{} {}".format(point.x, point.y)
    else:
      path += " L{} {}".format(point.x, point.y)

  # Path line
  # lib.path(path)

  positions = []

  # Draw start circle
  if circle:
    add_nondup_position(clamp(points[0].x), clamp(points[0].y), size_min, positions)
  else:
    x = points[0].x - size_min
    y = points[0].y - size_min
    add_nondup_position(clamp(x), clamp(y), size_min * 2, positions)
  size = size_min
  next_size = 0

  # Add positions
  for i in range(1, len(points)):
    next_size = random.randrange(size_min, size_max)
    if i == len(points) - 1:
      next_size = size_min

    p0 = points[i - 1]
    p1 = points[i]
    vector = p1.subtract(p0)
    length = vector.length()
    vector.normalize()

    copy = vector.multiply_copy(step_dist)
    copy_len = copy.length()
    while copy_len < length:
      step_size = lib.ease_in_out_quad(copy_len, size, next_size - size, length)
      # step_size = lib.lerp(size, next_size, copy_len / length)
      if circle:
        add_nondup_position(clamp(p0.x + copy.x), clamp(p0.y + copy.y), step_size, positions)
      else:
        x = p0.x + copy.x - step_size
        y = p0.y + copy.y - step_size
        add_nondup_position(clamp(x), clamp(y), step_size * 2, positions)
      copy = vector.multiply_copy(copy_len + step_dist)
      copy_len = copy.length()

    if circle:
      add_nondup_position(clamp(p1.x), clamp(p1.y), next_size, positions)
    else:
      x = p1.x - next_size
      y = p1.y - next_size
      add_nondup_position(clamp(x), clamp(y), next_size * 2, positions)
    size = next_size

  # Draw actual items
  for pos in positions:
    if circle:
      lib.circ(pos.x, pos.y, pos.size)
    else:
      lib.rect(pos.x, pos.y, pos.size, pos.size)


seed = 0
test = True
image_size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  lib.main(
    "long-worm",
    test,
    seed,
    image_size,
    loop
  )
