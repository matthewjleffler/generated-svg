from lib import *
from math import *


def loop():
  # draw_border()

  count = 20
  clamp_start = 50
  circles = []

  for _ in range(count):
    x = random.randrange(svg_safe().x, svg_safe().w)
    y = random.randrange(svg_safe().y, svg_safe().h)

    x = round(x / clamp_start, 0) * clamp_start
    y = round(y / clamp_start, 0) * clamp_start

    add_nondup_point(x, y, circles)

    # Debug show origins
    draw_rect(x, y, 10, 10)

  circles.sort()

  for point in circles:
    stack_count = random.randint(35, 35)
    max_size = random.randint(50, 150)

    for i in range(0, stack_count + 1):
      percent = i / stack_count
      pi_percent = percent * pi

      size = 10 + sin(pi_percent) * max_size
      half = size / 2

      x = point.x + 10 * i
      y = point.y + 10 * i
      if not svg_safe().contains(x - half, y - half) or not svg_safe().contains(x + half, y + half):
        continue

      draw_circ(x, y, half)

test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("circle-stack", test, seed, size, loop)

