from lib_spiral import *


def loop_combined():
  params = SpiralParams()
  draw_spiral(params)
  return params

def loop_main():
  params = SpiralParams()
  params.draw_border = False
  draw_spiral(params)
  return params

def loop_highlights():
  params = SpiralParams()
  params.draw_circles = False
  draw_spiral(params)
  return params


dir = "spiral-circles"
seed = 0
test = True
size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "combined", test, seed, size, loop_combined)
  main(dir, "main", test, mainseed, size, loop_main)
  main(dir, "highlights", test, mainseed, size, loop_highlights)

if __name__ == "__main__":
  run()

