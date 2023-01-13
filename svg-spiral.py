from lib_spiral import *


def loop_combined():
  params = SpiralParams()
  draw_spiral(params)

def loop_main():
  params = SpiralParams()
  params.draw_border = False
  draw_spiral(params)

def loop_highlights():
  params = SpiralParams()
  params.draw_circles = False
  draw_spiral(params)


dir = "spiral-circles"
seed = 0
test = True
size = SvgSize.Size9x12

if __name__ == "__main__":
  real_seed = main(dir, "combined", test, seed, size, loop_combined)
  main(dir, "main", test, real_seed, size, loop_main)
  main(dir, "highlights", test, real_seed, size, loop_highlights)

