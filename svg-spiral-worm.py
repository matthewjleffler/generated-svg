from worm import *

def loop_combined():
  # draw_border()

  params = SprialWormParams()
  draw_spiral_worm(params)

def loop_worm():
  # draw_border()

  params = SprialWormParams()
  params.draw_highlight = False
  params.draw_highlight2 = False
  draw_spiral_worm(params)

def loop_highlight():
  # draw_border()

  params = SprialWormParams()
  params.draw_worm = False
  params.draw_highlight2 = False
  draw_spiral_worm(params)

def loop_highlight_2():
  # draw_border()

  params = SprialWormParams()
  params.draw_worm = False
  params.draw_highlight = False
  draw_spiral_worm(params)

seed = 0
test = True
image_size = SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = main("spiral-worm-combined", test, seed, image_size, loop_combined)
  main("spiral-worm-worm", test, mainseed, image_size, loop_worm)
  main("spiral-worm-highlight", test, mainseed, image_size, loop_highlight)
  main("spiral-worm-highlight-layer", test, mainseed, image_size, loop_highlight_2)
