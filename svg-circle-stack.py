import lib
import random


def loop():
  # Border
  # lib.rect(lib.svg_safe.x, lib.svg_safe.y, lib.svg_safe.w, lib.svg_safe.h, "red")

  count = 50
  stack_count = 30
  # count = random.randrange(20, 100)
  # print("Circles: {}".format(count))

  circles = []

  for _ in range(count):
    x = random.randrange(0, lib.svg_full.w)
    y = random.randrange(0, lib.svg_full.h)

    x = round(x / 10, 0) * 10
    y = round(y / 10, 0) * 10

    for i in range(0, stack_count + 1):
      lib.add_nondup_point(x + i * 10, y + i * 10, circles)

  circles.sort()

  for point in circles:
    # size = random.randrange(40, 60)
    size = 100
    size = round(size / 10, 0) * 10
    half = size / 2

    x = point.x
    y = point.y
    if not lib.svg_safe.contains(x - half, y - half) or not lib.svg_safe.contains(x + half, y + half):
      continue

    lib.circ(x, y, half)

if __name__ == "__main__":
  lib.main(
    "circle-stack",
    False,
    6541782735430617851,
    lib.SvgSize.Size9x12,
    loop
  )

