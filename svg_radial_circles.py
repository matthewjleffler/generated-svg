from lib_radial_circle import *


def loop_combined():
  params = RadialParams()
  draw_radial_circles(params)
  return params

def loop_main():
  params = RadialParams()
  params.draw_border = False
  draw_radial_circles(params)
  return params

def loop_highlights():
  params = RadialParams()
  params.draw_circles = False
  draw_radial_circles(params)
  return params


dir = "radial-circles"
seed = 0
test = True
size = SvgSize.Size9x12

def run():
  mainseed = main(dir, "combined", test, seed, size, loop_combined)
  main(dir, "main", test, mainseed, size, loop_main)
  main(dir, "highlights", test, mainseed, size, loop_highlights)

if __name__ == "__main__":
  run()

