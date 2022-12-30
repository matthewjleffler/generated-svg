import lib
import random
import math


def loop():
  # lib.border()

  count = 1
  clamp_start = 50
  circles = []

  for _ in range(count):
    x = random.randrange(lib.svg_safe.x, lib.svg_safe.w)
    y = random.randrange(lib.svg_safe.y, lib.svg_safe.h)

    x = round(x / clamp_start, 0) * clamp_start
    y = round(y / clamp_start, 0) * clamp_start

    lib.add_nondup_point(x, y, circles)

    # Debug show origins
    # lib.rect(x, y, 10, 10, "red")

  circles.sort()

  for point in circles:
    stack_count = random.randint(35, 35)
    max_size = random.randint(50, 150)

    for i in range(0, stack_count + 1):
      percent = i / stack_count
      pi_percent = percent * math.pi

      size = 10 + math.sin(pi_percent) * max_size
      half = size / 2

      x = point.x + 10 * i
      y = point.y + 10 * i
      if not lib.svg_safe.contains(x - half, y - half) or not lib.svg_safe.contains(x + half, y + half):
        continue

      lib.circ(x, y, half)

if __name__ == "__main__":
  lib.main(
    "circle-stack",
    True,
    0,
    lib.SvgSize.Size11x17,
    loop
  )

