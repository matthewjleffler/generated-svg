from lib_worm import *


def loop_combined():
  params = LongWormParams()
  draw_long_worm(params)

def loop_main():
  params = LongWormParams()
  params.draw_highlight = False
  draw_long_worm(params)

def loop_highlight():
  params = LongWormParams()
  params.draw_worm = False
  draw_long_worm(params)


dir = "long-worm"
seed = 0
test = True
image_size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main(dir, "combined", test, seed, image_size, loop_combined)
  main(dir, "main", test, mainseed, image_size, loop_main)
  main(dir, "highlight", test, mainseed, image_size, loop_highlight)

