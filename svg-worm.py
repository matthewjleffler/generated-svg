from worm import *


def loop_worm():
  # draw_border()

  params = WormParams()
  draw_worm(params)


def loop_innards():
  #draw_border()

  params = WormParams()
  params.fixed_size = 5
  draw_worm(params)


seed = 0
test = True
size = SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = main("worm", test, seed, size, loop_worm)
  main("worm-innards", test, mainseed, size, loop_innards)

