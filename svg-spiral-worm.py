from lib_worm import *


def loop_combined():
  params = SprialWormParams()
  draw_spiral_worm(params)

def loop_main():
  params = SprialWormParams()
  params.draw_highlight = False
  params.draw_highlight2 = False
  draw_spiral_worm(params)

def loop_circle():
  params = SprialWormParams()
  params.draw_worm = False
  params.draw_highlight2 = False
  draw_spiral_worm(params)

def loop_lines():
  params = SprialWormParams()
  params.draw_worm = False
  params.draw_highlight = False
  draw_spiral_worm(params)


dir = "spiral-worm"
seed = 0
test = True
image_size = SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = main(dir, "combined", test, seed, image_size, loop_combined)
  main(dir, "main", test, mainseed, image_size, loop_main)
  main(dir, "circle", test, mainseed, image_size, loop_circle)
  main(dir, "lines", test, mainseed, image_size, loop_lines)
