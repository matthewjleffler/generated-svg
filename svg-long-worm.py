import lib
import random
import math

padding = 50
stack_count = 50
min_size_range = 5
max_size_range = 100
stack_spread = 3
# worm_size = max_col = max_row = 0


# def draw_worm(fixed_size):
#   for row in range(0, max_row):
#     origin_y = worm_size * row * 1.5

#     for col in range(0, max_col):
#       max_size = random.randrange(min_size_range, max_size_range)
#       origin_x = worm_size * col

#       # Debug bounds
#       # lib.rect(lib.svg_safe.x + origin_x, lib.svg_safe.y + origin_y, worm_size, worm_size)

#       for i in range(0, stack_count + 1):
#         percent = i / stack_count
#         pi_percent = percent * math.pi
#         pi_half_percent = percent * math.pi * .25

#         size = math.sin(pi_percent) * max_size
#         if fixed_size != 0:
#           size = min(fixed_size, size)

#         half = size / 2

#         x = lib.svg_safe.x + origin_x + math.sin(pi_half_percent) * stack_spread * i
#         y = lib.svg_safe.y + origin_y + math.cos(pi_half_percent) * stack_spread * i

#         lib.circ(x, y, half)


def loop():
  # global max_col, max_row, worm_size

  lib.border()


  points = []
  down = True
  padding = 50
  jump_x_min = 2
  jump_x_max = 20
  jump_y_min = 30
  jump_y_max = 50

  top = lib.svg_safe.y + padding
  bottom = lib.svg_safe.bottom() - padding

  last_x = lib.svg_safe.x + padding
  last_y = random.randrange(top, bottom)
  points.append(lib.Point(last_x, last_y))

  while last_x < lib.svg_safe.right() - padding:
    last_x += random.randrange(jump_x_min, jump_x_max)
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

    last_y = new_y
    points.append(lib.Point(last_x, last_y))

  path = ""
  for i in range(len(points)):
    point = points[i]
    if i == 0:
      path += "M{} {}".format(point.x, point.y)
    else:
      path += " L{} {}".format(point.x, point.y)

  # Draw worm path
  lib.path(path)

  # worm_size = stack_count * stack_spread * .75
  # worm_row_size = worm_size * 1.55

  # pad_x = lib.svg_safe.w - padding
  # pad_y = lib.svg_safe.h - padding

  # max_col = math.floor(pad_x / worm_size)
  # max_row = math.floor(pad_y / worm_row_size)

  # offset_x = (lib.svg_safe.w - (max_col * worm_size)) / 2
  # offset_y = (lib.svg_safe.h - (max_row * worm_row_size)) / 2

  # lib.open_group("transform=\"translate({},{})\"".format(offset_x, offset_y))
  # draw_worm(fixed_size)
  # lib.close_group()
  # lib.open_group("transform=\"translate({},{}) scale(-1,1)\"".format(lib.svg_full.w - offset_x + worm_size * .1, offset_y + worm_size * .75))
  # draw_worm(fixed_size)
  # lib.close_group()


seed = 0
test = True
image_size = lib.SvgSize.Size11x17

if __name__ == "__main__":
  lib.main(
    "long-worm",
    test,
    seed,
    image_size,
    loop
  )
