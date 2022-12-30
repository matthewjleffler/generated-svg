import lib
import random


def loop():
  # lib.border()

  count = 20
  stack_count = 15
  rects = []

  for _ in range(count):
    x = random.randrange(0, lib.svg_full.w)
    y = random.randrange(0, lib.svg_full.h)

    x = round(x / 10, 0) * 10
    y = round(y / 10, 0) * 10

    for i in range(0, stack_count + 1):
      lib.add_nondup_point(x + i * 10, y + i * 10, rects)

  rects.sort()

  for point in rects:
    # size = random.randrange(40, 60)
    size = 100
    size = round(size / 10, 0) * 10
    half = size / 2

    x = point.x - half
    y = point.y - half

    if not lib.svg_safe.contains(x, y) or not lib.svg_safe.contains(x + size, y + size):
      continue

    lib.rect(x, y, size, size)

if __name__ == "__main__":
  lib.main(
    "stack",
    True,
    0,
    lib.SvgSize.Size9x12,
    loop
  )

