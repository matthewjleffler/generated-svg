import lib
import text
import math

def loop():
  lib.border()

  size = 50
  bias_x = 135
  bias_y = 20

  count_horiz = math.floor(lib.svg_safe.w / size)
  count_vert = math.floor(lib.svg_safe.h / size)

  for i in range(0, count_horiz):
    path = f"M{lib.svg_safe.x + i * size} {lib.svg_safe.y}l{bias_x} {lib.svg_safe.h}"
    lib.path(path)

  for i in range(0, count_vert):
    path = f"M{lib.svg_safe.x} {lib.svg_safe.y + size + i * size}l{lib.svg_safe.w} {bias_y}"
    lib.path(path)

seed = 0
test = True
size = lib.SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = lib.main("checkerboard", test, seed, size, loop)

