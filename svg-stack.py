from lib import *

def loop():
  # draw_border()

  count = 20
  stack_count = 15
  rects = []

  for _ in range(count):
    x = rand_int(0, svg_full().w)
    y = rand_int(0, svg_full().h)

    x = round(x / 10, 0) * 10
    y = round(y / 10, 0) * 10

    for i in range(0, stack_count + 1):
      add_nondup_point(x + i * 10, y + i * 10, rects)

  rects.sort()

  for point in rects:
    # size = rand_int(40, 60)
    size = 100
    size = round(size / 10, 0) * 10
    half = size / 2

    x = point.x - half
    y = point.y - half

    if not svg_safe().contains(x, y) or not svg_safe().contains(x + size, y + size):
      continue

    draw_rect(x, y, size, size)

test = True
seed = 0
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("stack", test, seed, SvgSize.Size9x12, loop)

