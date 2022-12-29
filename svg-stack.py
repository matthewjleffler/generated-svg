import lib
import random

class Point:
  def __init__(self, x, y):
    self.x = x
    self.y = y

  def __lt__(self, other):
    if self.x == other.x:
      return self.y < other.y
    return self.x < other.x


def add_nondup_point(x, y, rects):
  for point in rects:
    if point.x == x and point.y == y:
      return
  rects.append(Point(x, y))


def loop():
  # Border
  # lib.rect_safe(0, 0, lib.svg_safe_width, lib.svg_safe_height, "red")

  count = 40
  stack_count = 9
  # count = random.randrange(20, 100)
  # print("Rectangles: {}".format(count))

  rects = []

  for _ in range(count):
    x = random.randrange(0, lib.svg_safe_width - 100 - 10 * max(stack_count - 1, 0))
    y = random.randrange(0, lib.svg_safe_height - 100 - 10 * max(stack_count - 1, 0))

    x = round(x / 10, 0) * 10
    y = round(y / 10, 0) * 10

    for i in range(0, stack_count):
      add_nondup_point(x + i * 10, y + i * 10, rects)

  rects.sort()

  for point in rects:
    lib.rect_safe(point.x, point.y, 100, 100)

if __name__ == "__main__":
  lib.main(
    "stack",
    True,
    0,
    lib.SvgSize.Size9x12,
    loop
  )

