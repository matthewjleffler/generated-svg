import lib
import random
import math


max_row = 5
max_col = 10
padding = 100
stack_count = 10
spread_x = spread_y = 0
min_size_range = 10
max_size_range = 50


def draw_worm(fixed_size):
  for row in range(0, max_row):
    origin_y = spread_y * row * 2

    for col in range(0, max_col):
      max_size = random.randrange(min_size_range, max_size_range)
      origin_x = spread_x * col

      for i in range(0, stack_count + 1):
        percent = i / stack_count
        pi_percent = percent * math.pi
        pi_half_percent = percent * math.pi * .2

        size = math.sin(pi_percent) * max_size
        if fixed_size != 0:
          size = min(fixed_size, size)

        half = size / 2

        x = lib.svg_safe.x + origin_x + math.sin(pi_half_percent) * 10 * i
        y = lib.svg_safe.y + origin_y + math.cos(pi_half_percent) * 10 * i

        lib.circ(x, y, half)


def loop(fixed_size):
  global spread_x, spread_y

  lib.border()

  spread_x = (lib.svg_safe.w - padding) / max_col
  spread_y = (lib.svg_safe.h - padding) / (max_row * 2.1)

  lib.open_group("transform=\"translate({},{})\"".format(padding / 2, padding / 2))
  draw_worm(fixed_size)
  lib.open_group("transform=\"translate({},{}) scale(-1,1)\"".format(lib.svg_safe.w, spread_y))
  draw_worm(fixed_size)


def loop_worm():
  loop(0)


def loop_innards():
  loop(5)


if __name__ == "__main__":
  lib.main(
    "worm",
    True,
    0,
    lib.SvgSize.Size9x12,
    loop_worm
  )

  lib.main(
    "worm-innards",
    True,
    1,
    lib.SvgSize.Size9x12,
    loop_innards
  )

