import lib
import random
import math

padding = 50
stack_count = 50
min_size_range = 5
max_size_range = 100
stack_spread = 3
worm_size = max_col = max_row = 0


def draw_worm(fixed_size):
  for row in range(0, max_row):
    origin_y = worm_size * row * 1.5

    for col in range(0, max_col):
      max_size = random.randrange(min_size_range, max_size_range)
      origin_x = worm_size * col

      # Debug bounds
      # lib.rect(lib.svg_safe.x + origin_x, lib.svg_safe.y + origin_y, worm_size, worm_size)

      for i in range(0, stack_count + 1):
        percent = i / stack_count
        pi_percent = percent * math.pi
        pi_half_percent = percent * math.pi * .25

        size = math.sin(pi_percent) * max_size
        if fixed_size != 0:
          size = min(fixed_size, size)

        half = size / 2

        x = lib.svg_safe.x + origin_x + math.sin(pi_half_percent) * stack_spread * i
        y = lib.svg_safe.y + origin_y + math.cos(pi_half_percent) * stack_spread * i

        lib.circ(x, y, half)


def loop(fixed_size):
  global max_col, max_row, worm_size

  # lib.border()

  worm_size = stack_count * stack_spread * .75
  worm_row_size = worm_size * 1.55

  pad_x = lib.svg_safe.w - padding
  pad_y = lib.svg_safe.h - padding

  max_col = math.floor(pad_x / worm_size)
  max_row = math.floor(pad_y / worm_row_size)

  offset_x = (lib.svg_safe.w - (max_col * worm_size)) / 2
  offset_y = (lib.svg_safe.h - (max_row * worm_row_size)) / 2

  lib.open_group("transform=\"translate({},{})\"".format(offset_x, offset_y))
  draw_worm(fixed_size)
  lib.close_group()
  lib.open_group("transform=\"translate({},{}) scale(-1,1)\"".format(lib.svg_full.w - offset_x + worm_size * .1, offset_y + worm_size * .75))
  draw_worm(fixed_size)
  lib.close_group()


def loop_worm():
  loop(0)


def loop_innards():
  loop(5)


seed = 0
test = True
image_size = lib.SvgSize.Size11x17

if __name__ == "__main__":
  lib.main(
    "worm",
    test,
    seed,
    image_size,
    loop_worm
  )

  lib.main(
    "worm-innards",
    test,
    seed,
    image_size,
    loop_innards
  )

