from lib import *
from math import *


def loop():
  draw_border()

  size = 50
  bias_x = 135
  bias_y = 20

  count_horiz = floor(svg_safe().w / size)
  count_vert = floor(svg_safe().h / size)

  for i in range(0, count_horiz):
    path = f"M{svg_safe().x + i * size} {svg_safe().y}l{bias_x} {svg_safe().h}"
    draw_path(path)

  for i in range(0, count_vert):
    path = f"M{svg_safe().x} {svg_safe().y + size + i * size}l{svg_safe().w} {bias_y}"
    draw_path(path)


seed = 0
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("checkerboard", test, seed, size, loop)

