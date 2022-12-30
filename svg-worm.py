import lib
import random
import math


def loop():
  # lib.border()

  spread_border = 20
  border_x = 10
  border_y = 0
  spread_x = 200
  spread_y = 115
  row_2_offset = 190

  for row in range(0, 6):
    origin_y = spread_border + spread_y * row

    for col in range(0, 5):
      stack_count = 20
      max_size = random.randrange(20, 75)

      origin_x = spread_border + spread_x * col

      if row % 2 == 1:
        origin_x += row_2_offset

      for i in range(0, stack_count + 1):
        percent = i / stack_count
        pi_percent = percent * math.pi
        pi_half_percent = percent * math.pi * .25

        size = 10 + math.sin(pi_percent) * max_size
        half = size / 2

        if row % 2 == 0:
          x = lib.svg_safe.x + border_x + origin_x + math.sin(pi_half_percent) * 10 * i
          y = lib.svg_safe.y + border_y + origin_y + math.cos(pi_half_percent) * 10 * i
        else:
          x = lib.svg_safe.x + border_x + origin_x - math.sin(pi_half_percent) * 10 * i
          y = lib.svg_safe.x + border_y + origin_y + math.cos(pi_half_percent) * 10 * i

        lib.circ(x, y, half)


if __name__ == "__main__":
  lib.main(
    "worm",
    True,
    0,
    lib.SvgSize.Size9x12,
    loop
  )

