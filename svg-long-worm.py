from worm import *


def loop_combined():
  # draw_border()

  params = LongWormParams()
  draw_long_worm(params)

def loop_worm():
  # draw_border()

  params = LongWormParams()
  params.draw_highlight = False
  draw_long_worm(params)

def loop_highlight():
  # draw_border()

  params = LongWormParams()
  params.draw_worm = False
  draw_long_worm(params)


seed = 0
test = True
image_size = SvgSize.Size9x12

if __name__ == "__main__":
  mainseed = main("long-worm-combined", test, seed, image_size, loop_combined)
  main("long-worm-worm", test, mainseed, image_size, loop_worm)
  main("long-worm-highlight", test, mainseed, image_size, loop_highlight)

