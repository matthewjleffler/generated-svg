from lib_worm import *


def loop_combined():
  params = WormParams()
  draw_worm(params)

def loop_main():
  params = WormParams()
  params.draw_innards = False
  draw_worm(params)

def loop_innards():
  params = WormParams()
  params.draw_worm = False
  draw_worm(params)


dir = "worm"
seed = 0
test = True
size = SvgSize.Size11x17

if __name__ == "__main__":
  mainseed = main(dir, "combined", test, seed, size, loop_combined)
  main(dir, "main", test, mainseed, size, loop_main)
  main(dir, "innards", test, mainseed, size, loop_innards)

